import json
from time import sleep
import uuid
from yookassa import Configuration,Payment


class PaymentYookassa:


    def __init__(self, value,  description):
        self.value = value  # Here transfer the payment amount.  
        self.description = description 

    def get_pay_link(self):
        """Creating a payment instance, returning information about the created payment.  """

        Configuration.account_id = "205041"
        Configuration.secret_key = "test_0bcnDHPvWOvEq7x05H_FzpjPbbceNj4-vYp51hAWLP0" 

        #creating a payment
        payment = Payment.create({
                                "amount": {
                                        "value": self.value,
                                        "currency": "RUB" 
                                        },
                                "confirmation": { 
                                                "type": "redirect", 
                                                "return_url": "https://www.return_url" 
                                                },
                                "capture": True, 
                                "description": self.description 
                                }, uuid.uuid4())

        
        payment_data = json.loads(payment.json()) # Get data about the created payment.  
        payment_url = (payment_data['confirmation'])['confirmation_url'] # Link for payment.  
        print(payment_url)
        
        return payment
    
    
    def chek_payment(self, payment):
        """Checking the status of the created payment. """

        payment_data = json.loads(payment.json()) 
        payment_id = payment_data['id'] 
        payment_status =(payment_data['status']) 


        while payment_status == 'pending': 
            payment_data = json.loads(Payment.find_one(payment_id).json())
            payment_status = (payment_data['status'])
            sleep(10) 
        
        if payment_status == 'succeeded': 
            print("The payment was successful")    
            return True
            
        else:
            print("Something  wrong") 
            return False




p = PaymentYookassa(100, "description")

print(p.chek_payment(p.get_pay_link()))

