def test_vat_calculation():
    line_total = 1000  
    vat_rate = 20.0
    vat = round(line_total * vat_rate / 100)
    assert vat == 200

def test_service_charge_calculation():
    subtotal = 1000  
    service_charge = round(subtotal * 0.1)
    assert service_charge == 100

def test_total_calculation():
    subtotal = 1000
    service_charge = 100
    vat = 200
    total = subtotal + service_charge + vat
    assert total == 1300