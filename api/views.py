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
                    "err-message":"table_number and covers are required"}, status=status.HTTP_400_BAD_REQUEST)
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
    pass

class AddTabItemView(APIView):
    pass

class CreatePaymentIntentView(APIView):
    pass

class TakePaymentView(APIView):
    pass
