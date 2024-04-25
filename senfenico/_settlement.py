from dataclasses import dataclass, field
import requests
import json
from typing import Union, List, Optional
from senfenico.utils import SenfenicoJSONEncoder

@dataclass
class SettlementData:
    reference: str
    amount: int
    settlement_fees: float
    currency: str
    status: str
    live_mode: bool
    created_at: str
    updated_at: str
    account_type: str
    iban: str
    rib: str
    bank_name: str
    bank_address: str
    account_holder_name: str
    account_holder_address: str
    swift_bic_code: str
    provider: str
    phone: str
    usdt_wallet_address: str

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=12)

    def __repr__(self):
        return self.__str__()



@dataclass
class SenfenicoObject:
    status: bool
    message: str
    data: Union[SettlementData, List[SettlementData]]
    errors: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict.get('data')
        if isinstance(data, dict):
            data_obj = SettlementData(**data)
        elif isinstance(data, list):
            data_obj = [SettlementData(**item) for item in data]
        else:
            data_obj = None
        return cls(status=data_dict['status'], message=data_dict['message'], errors=data_dict.get('errors'), data=data_obj)


    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=4)

    def __repr__(self):
        return self.__str__()


class Settlement:

    @classmethod
    def create(cls, amount: int) -> SenfenicoObject:
        from senfenico import api_key
        
        url = "https://api.senfenico.com/v1/payment/settlements/"

        payload = json.dumps({
            "amount": amount
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }
        
        response = requests.post(url, headers=headers, data=payload)
        settlement = SenfenicoObject.from_dict(response.json())
        return settlement
    

    @classmethod
    def fetch(cls, settlement_reference) -> SenfenicoObject:
        from senfenico import api_key
        url = f"https://api.senfenico.com/v1/payment/settlements/{settlement_reference}"

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
        url = "https://api.senfenico.com/v1/payment/settlements"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers, data=payload)
        charge_list = SenfenicoObject.from_dict(response.json())
        return charge_list
    

    @classmethod
    def cancel(cls, settlement_reference) -> SenfenicoObject:
        from senfenico import api_key
        url = f"https://api.senfenico.com/v1/payment/settlements/{settlement_reference}/cancel/"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers, data=payload)
        cancelled_settlement = SenfenicoObject.from_dict(response.json())
        return cancelled_settlement
    
