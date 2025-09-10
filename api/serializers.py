from rest_framework import serializers
from .models import Tab, TabItem

class PostTabSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(required=False)
    table_number = serializers.IntegerField(required=True)
    covers = serializers.IntegerField(required=True, min_value=1)
    class Meta:
        model = Tab
        fields = ["id", "table_number", "covers"]

class TabItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="menu_item.name")

    class Meta:
        model = TabItem
        fields = ["name", "qty", "unit_price_p", "vat_rate_percent", "vat_p", "line_total_p"]
        
class TableDetailSerializer(serializers.ModelSerializer):
        id=serializers.IntegerField(required=False)
        items= TabItemSerializer(many=True)
        subtotal_p= serializers.IntegerField(required=True)
        service_charge_p= serializers.IntegerField(required=True)
        vat_total_p = serializers.IntegerField(required=True)
        total_p = serializers.IntegerField(required=True)
        
        class Meta:
            model = TabItem
            fields = ["id", "items", "subtotal_p","service_charge_p","vat_total_p","total_p"]
            
class TabItemResponseSerializer(serializers.ModelSerializer):
    qty = serializers.IntegerField(min_value=1)

    class Meta:
            model = TabItem
            fields = ["id", "menu_item_id", "qty"]

   