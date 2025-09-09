from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tab, TabItem, MenuItem, Payment

class PostTabView(APIView):
    def post(self, request):
        
        table_number=request.data.get('table_number')
        covers=request.data.get('covers')
        
        if table_number is None or covers is None:
            return Response({
                    "error":"table_number and covers are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:           
            tab=Tab.objects.create(
                table_number=int(table_number),
                covers=int(covers)
                )
            
            return Response({
                "id":tab.id,
                "table_number":tab.table_number,
                'covers': tab.covers,
                'status': tab.status
            },status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class TabDetailView(APIView):
    def get(self,request,tab_id):
        try:
            tab=Tab.objects.get(id=tab_id)
            
            all_items=[]
            
            for item in tab.items.all():  
                all_items.append({
                    'name': item.menu_item.name,
                    'qty': item.qty,
                    'unit_price_p': item.unit_price_p,
                    'vat_rate_percent': float(item.vat_rate_percent),
                    'vat_p': item.vat_p,
                    'line_total_p': item.line_total_p
                })
            return Response({
                'id': tab.id,
                'table_number': tab.table_number,
                'covers': tab.covers,
                'status': tab.status,
                'items': all_items,
                'subtotal_p': tab.subtotal_p,
                'service_charge_p': tab.service_charge_p,
                'vat_total_p': tab.vat_total_p,
                'total_p': tab.total_p
            })
        except Tab.DoesNotExist:
            return Response({'error': 'Tab not found'}, status=status.HTTP_404_NOT_FOUND)
    

class AddTabItemView(APIView):
    pass

class CreatePaymentIntentView(APIView):
    pass

class TakePaymentView(APIView):
    pass
