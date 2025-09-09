from django.db import models

class MenuItem(models.Model):
    name= models.CharField(max_length=250)
    unit_price_p = models.IntegerField() 
    vat_rate_percent = models.DecimalField(max_digits=5,decimal_places=2)

class Tab(models.Model):
    STATUS_CHOICES = [
    ('OPEN', 'Open'),
    ('PAID', 'Paid'),
]
    table_number = models.IntegerField()
    covers = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    subtotal_p = models.IntegerField(default=0)
    service_charge_p = models.IntegerField(default=0)
    vat_total_p = models.IntegerField(default=0)
    total_p = models.IntegerField(default=0)

class TabItem(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    qty = models.IntegerField()
    unit_price_p = models.IntegerField()
    vat_rate_percent = models.DecimalField(max_digits=5, decimal_places=2) 
    vat_p = models.IntegerField()
    line_total_p = models.IntegerField()
    
class Payment(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE)
    payment_intent_id = models.CharField(max_length=255)
    amount_p = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)