from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tab, TabItem, MenuItem, Payment
from api.payment.gateway import MockGateway
from django.utils import timezone
from .serializers import PostTabSerializer, TableDetailSerializer, TabItemResponseSerializer

class PostTabView(APIView):
    def post(self, request):
        
        serializer = PostTabSerializer(data=request.data)

        if serializer.is_valid():
            tab = Tab.objects.create(**serializer.validated_data)
            
            serializer=PostTabSerializer(tab)
            
            return Response(
                    serializer.data,
                    status=201
                )
        else:
            return Response(
                {"error":"table_number and covers are required"},
                status=400
            )
        
class TabDetailView(APIView):
    def get(self,request,tab_id):
        try:
            tab=Tab.objects.get(id=tab_id)
            
            serializer = TableDetailSerializer(tab)
            
            return Response(serializer.data)
        
        except Tab.DoesNotExist:
            return Response({'error': 'Tab not found'}, status=404)
    
class AddTabItemView(APIView):
    def post(self, request, tab_id):
        
        
        menu_item_id = request.data.get('menu_item_id')
        qty_string = request.data.get('qty')
        
        if menu_item_id is None:
            return Response({'error': 'menu_item_id is required'}, status=400)
        
        if qty_string is None:
            return Response({'error': 'qty is required'}, status=400)
        
        try:
            qty=int(qty_string)

            tab=Tab.objects.get(id=tab_id)
            
            if tab.status == 'PAID':
                return Response({'error': 'Cannot add items to paid tab'}, status=400)
            
            menu_item = MenuItem.objects.get(id=menu_item_id)
            
            line_total = menu_item.unit_price_p * qty
            vat_amount = round(line_total * menu_item.vat_rate_percent / 100)
            
            tab_item = TabItem.objects.create(
                tab=tab,
                menu_item=menu_item,
                qty=qty,
                unit_price_p=menu_item.unit_price_p,  
                vat_rate_percent=menu_item.vat_rate_percent, 
                vat_p=vat_amount,
                line_total_p=line_total
            )
            tab.subtotal_p += line_total  
            tab.vat_total_p += vat_amount 
            tab.service_charge_p = round(tab.subtotal_p * 0.1) 
            tab.total_p = tab.subtotal_p + tab.service_charge_p + tab.vat_total_p
            tab.save()
            
            serialzer= TabItemResponseSerializer(tab_item)
            
            return Response(serialzer.data, status=201)
    
        except Tab.DoesNotExist:
            return Response({'error': 'Tab not found'}, status=404)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found'}, status=404)

class CreatePaymentIntentView(APIView):
    def post(self, request, tab_id):
        try:
            tab=Tab.objects.get(id=tab_id)
            
            if tab.status == 'PAID':
                return Response({'error': 'Tab already paid'}, status=400)
            if tab.total_p == 0:
                return Response({'error': 'Cannot pay empty tab'}, status=400)
            
            gateway=MockGateway()
            intent=gateway.create_payment_intent(tab.total_p)
            
            return Response({
                'id': intent['id'],
                'client_secret': intent['client_secret']
            }, status=201)
            
        except Tab.DoesNotExist:
            return Response({'error': 'Tab not found'}, status=404)
    
class TakePaymentView(APIView):
    def post(self,request,tab_id):
        try:
            tab=Tab.objects.get(id=tab_id)
            
            if tab.status=="PAID":
                return Response({'error': 'Tab already paid'}, status=400)
            
            intent_id = request.data.get('intent_id')
            if not intent_id:
                return Response({'error': 'intent_id required'}, status=400)
            
            gateway = MockGateway()
            result = gateway.confirm_payment_intent(intent_id)
            
            if result["status"]=="failed":
                return Response({
                    'error': 'Payment failed',
                    'reason': result.get('reason')
                }, status=402)
                
                
            tab.status = 'PAID'
            tab.closed_at = timezone.now()
            tab.save()
                
            Payment.objects.create(
                    tab=tab,
                    payment_intent_id=intent_id,
                    amount_p=tab.total_p,
                    status='SUCCEEDED'
                )
            return Response({'status': 'paid'})
        
        except Tab.DoesNotExist:
            return Response({'error': 'Tab not found'}, status=404)
