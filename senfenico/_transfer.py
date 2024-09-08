from dataclasses import dataclass, field
import requests
import json
from typing import Union, List, Optional, Dict
from senfenico.utils import SenfenicoJSONEncoder

@dataclass
class TransferData:
    reference: str
    amount: int
    fees: float
    currency: str
    ip_address: str
    status: str
    live_mode: bool
    recipient_wallet: str
    recipient_phone: str
    created_at: str
    ext_id: Optional[str] = None
    

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=12)

    def __repr__(self):
        return self.__str__()

@dataclass
class FailedTransferData:
    amount: Optional[int] = None
    recipient_phone: Optional[str] = None
    recipient_wallet: Optional[str] = None
    ext_id: Optional[str] = None

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=14)

    def __repr__(self):
        return self.__str__()

@dataclass
class FailedTransfer:
    data: FailedTransferData
    errors: Dict[str, List[str]]

    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict.get('data')
        transfer_data = FailedTransferData(**data)
        return cls(data=transfer_data, errors=data_dict['errors'])

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=12)

    def __repr__(self):
        return self.__str__()

@dataclass
class SenfenicoObject:
    status: bool
    message: str
    data: Union[TransferData, List[TransferData]]
    error_code: Optional[str] = None
    errors: Optional[str] = None
    #failed_transfers: Optional[str] = None
    failed_transfers: Optional[List[FailedTransfer]] = None

    def __post_init__(self):
        # Remove fields that are None
        if self.error_code is None:
            del self.__dict__['error_code']
        if self.errors is None:
            del self.__dict__['errors']
        if self.data is None:
            del self.__dict__['data']
        if self.failed_transfers is None:
            del self.__dict__['failed_transfers']

    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict.get('data')
        if isinstance(data, dict):
            data_obj = TransferData(**data)
        elif isinstance(data, list):
            data_obj = [TransferData(**item) for item in data]
        else:
            data_obj = None
        
        failed_transfers = data_dict.get('failed_transfers', [])
        failed_transfers_obj = [FailedTransfer.from_dict(ft) for ft in failed_transfers]

        return cls(
            status=data_dict['status'], 
            message=data_dict['message'], 
            data=data_obj, 
            error_code=data_dict.get('error_code'), 
            errors=data_dict.get('errors'), 
            failed_transfers=failed_transfers_obj if failed_transfers else None
            #failed_transfers=data_dict.get('failed_transfers')
        )

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=4)

    def __repr__(self):
        return self.__str__()


class Transfer:

    @classmethod
    def create(cls, amount: int, recipient_phone: str, recipient_wallet: str, ext_id: Optional[str] = None) -> SenfenicoObject:
        from senfenico import api_key
        
        url = "https://api.senfenico.com/v1/payment/transfers/"

        payload = {
            "amount": amount,
            "recipient_phone": recipient_phone,
            "recipient_wallet": recipient_wallet
        }
        if ext_id:
            payload["ext_id"] = ext_id
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        transfer = SenfenicoObject.from_dict(response.json())
        return transfer
    

    @classmethod
    def bulk_create(cls, transfers: List[dict]) -> SenfenicoObject:
        from senfenico import api_key
        
        url = "https://api.senfenico.com/v1/payment/transfers/bulk/"

        payload = {"transfers": transfers}
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        bulk_transfer = SenfenicoObject.from_dict(response.json())
        return bulk_transfer
    

    @classmethod
    def fetch(cls, transfer_reference: str) -> SenfenicoObject:
        from senfenico import api_key
        url = f"https://api.senfenico.com/v1/payment/transfers/{transfer_reference}"

        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers)
        fetched_transfer = SenfenicoObject.from_dict(response.json())
        return fetched_transfer


    @classmethod
    def list(cls) -> SenfenicoObject:
        from senfenico import api_key
        url = "https://api.senfenico.com/v1/payment/transfers/"

        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers)
        transfer_list = SenfenicoObject.from_dict(response.json())
        return transfer_list
