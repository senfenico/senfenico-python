from dataclasses import dataclass, field
import requests
import json
from typing import Union, List, Optional

@dataclass
class CheckoutData:
    email: str
    reference: str
    charge_reference: str
    amount: int
    success_url: str
    cancel_url: str
    phone: str
    provider: str
    live_mode: bool
    created_at: str
    updated_at: str
    status: str
    
    def __str__(self):
        return f'{{\n\t\t"email": {self.email},\n\t\t"reference": {self.reference},\n\t\t"charge_reference": {self.charge_reference},\n\t\t"amount": {self.amount},\n\t\t"success_url": {self.success_url},\n\t\t"cancel_url": {self.cancel_url},\n\t\t"phone": {self.phone},\n\t\t"provider": {self.provider},\n\t\t"live_mode": {self.live_mode},\n\t\t"created_at": {self.created_at},\n\t\t"updated_at": {self.status},\n\t\t"reference": {self.status}\n\t}}'

    def __repr__(self):
        return self.__str__()

@dataclass
class CheckoutInitData:
    reference: str
    authorization_url: str

    def __str__(self):
        return f'{{\n\t\t"reference": {self.reference},\n\t\t"authorization_url": {self.authorization_url}\n\t}}'

    def __repr__(self):
        return self.__str__()


@dataclass
class SenfenicoObject:
    status: bool
    message: str
    data: Union[CheckoutInitData, CheckoutData, List[CheckoutData]]
    errors: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict.get('data')
        if isinstance(data, dict):
            try:
                data_obj = CheckoutData(**data)
            except TypeError:
                data_obj = CheckoutInitData(**data)
        elif isinstance(data, list):
            data_obj = [CheckoutData(**item) for item in data]
        else:
            data_obj = None
        return cls(status=data_dict['status'], message=data_dict['message'], errors=data_dict.get('errors'), data=data_obj)



    def __str__(self):
        return f'{{\n\t"status": {self.status},\n\t"message": {self.message},\n\t"errors": {self.errors},\n\t"data": {self.data}\n}}'

    def __repr__(self):
        return self.__str__()


class Checkout:

    @classmethod
    def initialize(cls, amount: int, success_url: str = None, cancel_url: str = None, email: str = "customer@senfenico.com") -> SenfenicoObject:
        from senfenico import api_key
        
        url = "https://api.senfenico.com/v1/payment/checkouts/initialize/"

        payload = json.dumps({
        "email": email,
        "amount": amount,
        "success_url": success_url,
        "cancel_url": cancel_url
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
    def fetch(cls, checkout_reference) -> SenfenicoObject:
        from senfenico import api_key
        url = f"https://api.senfenico.com/v1/payment/checkouts/{checkout_reference}"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers, data=payload)

        fetched_checkout = SenfenicoObject.from_dict(response.json())

        return fetched_checkout


    @classmethod
    def list(cls) -> SenfenicoObject:
        from senfenico import api_key
        url = "https://api.senfenico.com/v1/payment/checkouts"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers, data=payload)

        checkout_list = SenfenicoObject.from_dict(response.json())

        return checkout_list
    
