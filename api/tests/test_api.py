import pytest
from rest_framework.test import APIClient
from api.models import Tab, MenuItem
from rest_framework import status

@pytest.fixture
def api_client():
    client=APIClient()
    client.defaults['HTTP_X_API_KEY'] = 'demo' 
    return client
@pytest.fixture
def menu_items():
    items = []
    items.append(MenuItem.objects.create(name="Flat White", unit_price_p=350, vat_rate_percent=20.0))
    items.append(MenuItem.objects.create(name="Croissant", unit_price_p=280, vat_rate_percent=0.0))
    return items
@pytest.fixture
def sample_tab():
    return Tab.objects.create(table_number=10, covers=4)

@pytest.mark.django_db
def test_API_validation():
    client = APIClient()
    payload={
        'table_number': 12,
        'covers': 2
        }
    response=client.post("/api/tabs/",payload)
    assert response.status_code==401
    assert response.json()["error"]== "Invalid API key"
    
@pytest.mark.django_db
def test_post_tab(api_client):
    payload={
        'table_number': 12,
        'covers': 2
        }
    response=api_client.post("/api/tabs/",payload)
    tab = Tab.objects.get(id=response.data['id']) 
    assert response.status_code==201
    assert response.data["table_number"]==12
    assert response.data["covers"]==2
    assert tab.table_number == 12
    
def test_create_tab_400(api_client):
    payload={
        'table_number': 12,
        }
    response=api_client.post("/api/tabs/",payload)
    assert response.status_code==400
    assert response.data["error"]=="table_number and covers are required"
    
@pytest.mark.django_db
def test_get_tab_details(api_client,sample_tab):
    response=api_client.get(f"/api/tabs/{sample_tab.id}/")
    assert response.status_code==200
    assert response.data["id"]==sample_tab.id
    assert "subtotal_p" in response.data
    assert "service_charge_p" in response.data
    assert "vat_total_p" in response.data
    assert "total_p" in response.data
    assert "items" in response.data    
    
@pytest.mark.django_db
def test_get_tab_details_400(api_client):
    response=api_client.get("/api/tabs/999/")
    assert response.status_code==404
    assert response.data["error"]== 'Tab not found'
    
@pytest.mark.django_db
def test_add_tab_item(api_client, menu_items,sample_tab):
    payload={
        "menu_item_id": menu_items[0].id, 
        "qty": 2
        }
    response=api_client.post(f"/api/tabs/{sample_tab.id}/items/",payload)
    assert response.status_code==201
    assert response.data["menu_item_id"]==menu_items[0].id
    assert response.data["qty"] == 2
    sample_tab.refresh_from_db()  
    assert sample_tab.subtotal_p > 0 
    assert sample_tab.total_p > 0

@pytest.mark.django_db
def test_add_tab_item_400(api_client,sample_tab):
    payload={
        "qty": 2
        }
    response=api_client.post(f"/api/tabs/{sample_tab.id}/items/",payload)
    assert response.status_code==400
    assert response.data["error"]=='menu_item_id is required'

@pytest.mark.django_db
def test_add_tab_items_404(api_client,sample_tab):
    payload={
        "menu_item_id":1000,
        "qty": 2
        }
    response=api_client.post(f"/api/tabs/{sample_tab.id}/items/",payload)
    assert response.status_code==404
    assert response.data["error"]=="Menu item not found"
    
@pytest.mark.django_db
def test_create_payment_intent(api_client, sample_tab):
    sample_tab.total_p = 1500 
    sample_tab.save()    
    
    response=api_client.post(f"/api/tabs/{sample_tab.id}/payment_intent/")
    assert response.status_code==201
    assert response.status_code == 201
    assert 'id' in response.data
    assert 'client_secret' in response.data

@pytest.mark.django_db
def test_create_payment_intent_400(api_client,sample_tab):
    sample_tab.total_p = 1500 
    sample_tab.save() 
    
    response=api_client.post(f"/api/tabs/not_id/payment_intent/")
    assert response.status_code==404
    
@pytest.mark.django_db
def test_confirm_payment_intent(api_client,sample_tab):
    sample_tab.total_p = 1500
    sample_tab.save()
    
    pi_response = api_client.post(f'/api/tabs/{sample_tab.id}/payment_intent/')
    assert pi_response.status_code == 201
    intent_id = pi_response.data['id']
    
    response = api_client.post(f'/api/tabs/{sample_tab.id}/take_payment/', {
        'intent_id': intent_id
    })
    assert response.status_code == 200
    assert response.data['status'] == 'paid'
    sample_tab.refresh_from_db()  
    assert sample_tab.status=="PAID"
    

@pytest.mark.django_db
def test_confirm_payment_intent_402(api_client, sample_tab):
    sample_tab.total_p = 1500
    sample_tab.save()
    
    pi_response = api_client.post(f'/api/tabs/{sample_tab.id}/payment_intent/')
    assert pi_response.status_code == 201
    
    pi_response.data["id"] = "pi_13"
    
    response = api_client.post(f'/api/tabs/{sample_tab.id}/take_payment/', {
        'intent_id': pi_response.data["id"]
    })
    assert response.status_code==402
    assert response.data["error"]=='Payment failed'
    assert response.data["reason"]=="Insufficient funds"
    assert sample_tab.status=="OPEN"

@pytest.mark.django_db
def test_take_payment_idempotent(api_client, sample_tab):
    sample_tab.total_p = 1500
    sample_tab.save()
    
    pi_response = api_client.post(f'/api/tabs/{sample_tab.id}/payment_intent/')
    intent_id = pi_response.data['id']
    
    first_response = api_client.post(f'/api/tabs/{sample_tab.id}/take_payment/', {
        'intent_id': intent_id
    })
    assert first_response.status_code == 200
    
    second_response = api_client.post(f'/api/tabs/{sample_tab.id}/take_payment/', {
        'intent_id': intent_id
    })
    assert second_response.status_code == 400
    assert second_response.data["error"]=="Tab already paid"
    