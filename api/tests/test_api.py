import pytest
from rest_framework.test import APIClient
from api.models import Tab, MenuItem
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()
@pytest.fixture
def menu_items():
    MenuItem.objects.create(name="Flat White", unit_price_p=350, vat_rate_percent=20.0)
    MenuItem.objects.create(name="Croissant", unit_price_p=280, vat_rate_percent=0.0)
    
@pytest.mark.django_db
def test_create_tab(api_client):
    payload={
        'table_number': 12,
        'covers': 2
        }
    response=api_client.post("/api/tabs/",payload)
    tab = Tab.objects.get(id=response.data['id']) 
    assert response.status_code==201
    assert response.data["table_number"]==12
    assert response.data["covers"]==2
    assert response.data["status"]=="OPEN"
    assert tab.table_number == 12
def test_create_tab_400(api_client):
    payload={
        'table_number': 12,
        }
    response=api_client.post("/api/tabs/",payload)
    assert response.status_code==status.HTTP_400_BAD_REQUEST
    