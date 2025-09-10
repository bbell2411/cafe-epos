from rest_framework.response import Response

class MockGateway:
    def create_payment_intent(self, amount_p:int, currency:str="gbp")->dict:
        return {
            "id": "pi_123", 
            "client_secret": "secret_ac",
            "status": "requires_confirmation"
        }
    def confirm_payment_intent(self, intent_id:str)->dict:
        if intent_id.endswith('13'):
            return{"status": "failed", "reason": "Insufficient funds"}
        
        return {"id": intent_id, "status": "succeeded"}