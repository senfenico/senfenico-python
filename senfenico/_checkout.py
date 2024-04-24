from dataclasses import dataclass, field
import requests
import json
from typing import Union, List, Optional
from senfenico.utils import SenfenicoJSONEncoder
import json


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
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=8)

    def __repr__(self):
        return self.__str__()

@dataclass
class CheckoutInitData:
    reference: str
    authorization_url: str

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=8)

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
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=4)

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
    
