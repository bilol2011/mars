import requests
import json
from datetime import datetime
from django.conf import settings
from decimal import Decimal


class PaymeService:
    """
    Payme payment service integration
    """
    PAYME_URL = "https://checkout.paycom.uz"
    TEST_PAYME_URL = "https://test.paycom.uz"
    
    def __init__(self, merchant_id=None, key=None):
        self.merchant_id = merchant_id or getattr(settings, 'PAYME_MERCHANT_ID', '')
        self.key = key or getattr(settings, 'PAYME_KEY', '')
        self.is_test = getattr(settings, 'PAYME_TEST_MODE', True)
        self.base_url = self.TEST_PAYME_URL if self.is_test else self.PAYME_URL
    
    def create_payment(self, amount, order_id, description, return_url=None):
        """
        Create a payment link
        """
        params = {
            'm': self.merchant_id,
            'ac.order_id': order_id,
            'a': amount * 100,  # Payme uses tiyin (1 so'm = 100 tiyin)
            'c': description,
            'l': 'uz',
        }
        
        if return_url:
            params['cr'] = return_url
        
        # Generate URL
        url = f"{self.base_url}/?{self._generate_params(params)}"
        return url
    
    def _generate_params(self, params):
        """
        Generate URL parameters
        """
        from urllib.parse import urlencode
        return urlencode(params)
    
    def verify_webhook(self, data):
        """
        Verify Payme webhook signature
        """
        # In production, verify the signature using the key
        # Payme sends a signature in the headers
        # For now, return True for testing
        return True
    
    def generate_signature(self, data):
        """
        Generate signature for Payme requests
        """
        import hashlib
        import json
        
        # Sort the data and create a string
        sorted_data = sorted(data.items())
        data_string = json.dumps(sorted_data, separators=(',', ':'))
        
        # Create signature
        signature = hashlib.sha256((data_string + self.key).encode()).hexdigest()
        return signature


class ClickService:
    """
    Click payment service integration
    """
    CLICK_URL = "https://my.click.uz/services"
    TEST_CLICK_URL = "https://test.my.click.uz/services"
    
    def __init__(self, service_id=None, merchant_id=None, secret_key=None):
        self.service_id = service_id or getattr(settings, 'CLICK_SERVICE_ID', '')
        self.merchant_id = merchant_id or getattr(settings, 'CLICK_MERCHANT_ID', '')
        self.secret_key = secret_key or getattr(settings, 'CLICK_SECRET_KEY', '')
        self.is_test = getattr(settings, 'CLICK_TEST_MODE', True)
        self.base_url = self.TEST_CLICK_URL if self.is_test else self.CLICK_URL
    
    def create_payment(self, amount, order_id, description, return_url=None):
        """
        Create a payment link
        """
        params = {
            'service_id': self.service_id,
            'merchant_id': self.merchant_id,
            'amount': amount,
            'transaction_id': order_id,
            'description': description,
        }
        
        if return_url:
            params['return_url'] = return_url
        
        # Generate URL
        url = f"{self.base_url}/pay?{self._generate_params(params)}"
        return url
    
    def _generate_params(self, params):
        """
        Generate URL parameters
        """
        from urllib.parse import urlencode
        return urlencode(params)
    
    def verify_webhook(self, data):
        """
        Verify Click webhook signature
        """
        # Click sends a signature in the headers
        # Verify using the secret key
        # For now, return True for testing
        return True
    
    def generate_signature(self, data):
        """
        Generate signature for Click requests
        """
        import hashlib
        import json
        
        # Click signature format: md5(service_id + secret_key + transaction_id + amount)
        signature_string = f"{self.service_id}{self.secret_key}{data.get('transaction_id', '')}{data.get('amount', '')}"
        signature = hashlib.md5(signature_string.encode()).hexdigest()
        return signature
    
    def prepare_payment(self, amount, order_id, phone_number=None):
        """
        Prepare payment for Click
        """
        params = {
            'service_id': self.service_id,
            'merchant_id': self.merchant_id,
            'amount': amount,
            'transaction_id': order_id,
        }
        
        if phone_number:
            params['phone_number'] = phone_number
        
        # Generate signature
        params['sign'] = self.generate_signature(params)
        
        return params


class PaymentService:
    """
    Unified payment service
    """
    def __init__(self):
        self.payme = PaymeService()
        self.click = ClickService()
    
    def create_payment(self, payment_method, amount, order_id, description, return_url=None):
        """
        Create payment based on method
        """
        if payment_method == 'payme':
            return self.payme.create_payment(amount, order_id, description, return_url)
        elif payment_method == 'click':
            return self.click.create_payment(amount, order_id, description, return_url)
        else:
            raise ValueError(f"Unsupported payment method: {payment_method}")
