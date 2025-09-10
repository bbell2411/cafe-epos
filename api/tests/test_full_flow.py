import pytest
from rest_framework.test import APIClient
from api.models import MenuItem, Tab


@pytest.fixture
def api_client():
    return APIClient()
@pytest.fixture
def menu_items():
    items = []
    items.append(MenuItem.objects.create(name="Flat White", unit_price_p=350, vat_rate_percent=20.0))
    items.append(MenuItem.objects.create(name="Croissant", unit_price_p=280, vat_rate_percent=0.0))
    return items

@pytest.mark.django_db
def test_full_flow(api_client, menu_items):
    # create tab
    tab_response = api_client.post('/api/tabs/', {
        'table_number': 12, 'covers': 2
    })
    tab_id = tab_response.data['id']
    
    # add items to tab
    api_client.post(f'/api/tabs/{tab_id}/items/', {
        'menu_item_id': menu_items[0].id, 'qty': 2
    })
    
    # get total and create payment intent
    pi_response = api_client.post(f'/api/tabs/{tab_id}/payment_intent/')
    intent_id = pi_response.data['id']
    
    # confirm payment 
    confirmed_payment=api_client.post(f'/api/tabs/{tab_id}/take_payment/', {
        'intent_id': intent_id
    })
    assert confirmed_payment.status_code==200
    
    # make sure tab is marked as PAID
    tab=Tab.objects.get(id=tab_id)
    assert tab.status=="PAID"
    
    # ensure idempotency
    second_response = api_client.post(f'/api/tabs/{tab_id}/take_payment/', {
        'intent_id': intent_id
    })
    assert second_response.status_code == 400
    assert second_response.data["error"]=="Tab already paid"