from dataclasses import dataclass, field
import requests
import json
from typing import Union, List, Optional

@dataclass
class ChargeConfirmationAttempt:
    ip_address: str
    attempt_date: str
    confirmation_status: str

    def __str__(self):
        return f'''{{
                \t\t\t\t"ip_address": {self.ip_address},
                \t\t\t\t"attempt_date": {self.attempt_date},
                \t\t\t\t"confirmation_status": {self.confirmation_status}
                \t\t\t}}'''

    def __repr__(self):
        return self.__str__()

@dataclass
class ChargeData:
    reference: str
    amount: int
    fees: float
    currency: str
    transaction_date: str
    ip_address: str
    status: str
    live_mode: bool
    payment_method: str
    provider: str
    phone: str
    cancelled_at: str
    cancellation_reason: str
    created_at: str
    updated_at: str
    confirmation_attempts: Optional[list[ChargeConfirmationAttempt]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data_dict):
        confirmation_attempts = data_dict.get('confirmation_attempts')
        if isinstance(confirmation_attempts, list):
            data_obj = [ChargeConfirmationAttempt(**item) for item in confirmation_attempts]
        else:
            data_obj = None
        return cls(reference=data_dict.get('reference'), amount=data_dict.get('amount'), fees=data_dict.get('fees'), currency=data_dict.get('currency'), 
                   transaction_date=data_dict.get('transaction_date'), ip_address=data_dict.get('ip_address'), status=data_dict.get('status'),
                   live_mode=data_dict.get('live_mode'), payment_method=data_dict.get('payment_method'), provider=data_dict.get('provider'),
                   phone=data_dict.get('phone'), cancelled_at=data_dict.get('cancelled_at'), cancellation_reason=data_dict.get('cancellation_reason'),
                   created_at=data_dict.get('created_at'), updated_at=data_dict.get('updated_at'), confirmation_attempts=data_obj)

    def __str__(self):
        return f'''{{
            \t\t"reference": {self.reference},
            \t\t"amount": {self.amount},
            \t\t"fees": {self.fees},
            \t\t"amount": {self.amount},
            \t\t"currency": {self.currency},
            \t\t"transaction_date": {self.transaction_date},
            \t\t"ip_address": {self.ip_address},
            \t\t"status": {self.status},
            \t\t"live_mode": {self.live_mode},
            \t\t"payment_method": {self.payment_method},
            \t\t"provider": {self.provider},
            \t\t"phone": {self.phone},
            \t\t"cancelled_at": {self.cancelled_at}
            \t\t"cancellation_reason": {self.cancellation_reason}
            \t\t"created_at": {self.created_at}
            \t\t"updated_at": {self.updated_at}
            \t\t"confirmation_attempts": {self.confirmation_attempts}
            \t}}'''

    def __repr__(self):
        return self.__str__()

@dataclass
class ChargeCreateData:
    reference: str
    status: str
    display_text: str
    live_mode: bool

    def __str__(self):
        return f'{{\n\t\t"reference": {self.reference},\n\t\t"status": {self.status},\n\t\t"display_text": {self.display_text},\n\t\t"live_mode": {self.live_mode}\n\t}}'

    def __repr__(self):
        return self.__str__()


@dataclass
class SenfenicoObject:
    status: bool
    message: str
    data: Union[ChargeCreateData, ChargeData, List[ChargeData]]
    errors: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict.get('data')
        if isinstance(data, dict):
            try:
                data_obj = ChargeCreateData(**data)
            except TypeError:
                data_obj = ChargeData.from_dict(data)
        elif isinstance(data, list):
            data_obj = [ChargeData.from_dict(item) for item in data]
        else:
            data_obj = None
        return cls(status=data_dict['status'], message=data_dict['message'], errors=data_dict.get('errors'), data=data_obj)


    def __str__(self):
        return f'{{\n\t"status": {self.status},\n\t"message": {self.message},\n\t"errors": {self.errors},\n\t"data": {self.data}\n}}'

    def __repr__(self):
        return self.__str__()


class Charge:

    @classmethod
    def create(cls, amount: int, phone: str = None, provider: str = None, currency: str = "XOF", payment_method: str = "mobile_money") -> SenfenicoObject:
        from senfenico import api_key
        
        url = "https://api.senfenico.com/v1/payment/charges/"

        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "payment_method": payment_method,
            "payment_method_details": {
                "phone": phone,
                "provider": provider
            }
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }
        
        response = requests.post(url, headers=headers, data=payload)

        init_checkout = SenfenicoObject.from_dict(response.json())

        return init_checkout
    

    @classmethod
    def submit_otp(cls, otp: str, charge_reference: str = None) -> SenfenicoObject:
        from senfenico import api_key
        
        url = "https://api.senfenico.com/v1/payment/charges/submit"

        payload = json.dumps({
        "otp": otp,
        "charge_reference": charge_reference
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }
        
        response = requests.post(url, headers=headers, data=payload)

        init_checkout = SenfenicoObject.from_dict(response.json())

        return init_checkout


    @classmethod
    def fetch(cls, charge_reference) -> SenfenicoObject:
        from senfenico import api_key
        url = f"https://api.senfenico.com/v1/payment/charges/{charge_reference}"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers, data=payload)

        fetched_charge = SenfenicoObject.from_dict(response.json())

        return fetched_charge


    @classmethod
    def list(cls) -> SenfenicoObject:
        from senfenico import api_key
        url = "https://api.senfenico.com/v1/payment/charges"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers, data=payload)

        charge_list = SenfenicoObject.from_dict(response.json())

        return charge_list
    
