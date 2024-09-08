from dataclasses import dataclass
import requests
from typing import List, Optional
from senfenico.utils import SenfenicoJSONEncoder
import json

@dataclass
class CollectionBalanceData:
    available: float
    pending: float
    currency: str

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=8)

    def __repr__(self):
        return self.__str__()

@dataclass
class OperatorTransfBalanceData:
    available: float
    pending: float

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=8)

    def __repr__(self):
        return self.__str__()

@dataclass
class TransferBalanceData:
    total_available: float
    total_pending: float
    orange_money_bf: Optional[OperatorTransfBalanceData] = None
    moov_money_bf: Optional[OperatorTransfBalanceData] = None
    sank_money_bf: Optional[OperatorTransfBalanceData] = None

    @classmethod
    def from_dict(cls, data_dict):
        orange_money_bf = data_dict.get('orange_money_bf')
        moov_money_bf = data_dict.get('moov_money_bf')
        sank_money_bf = data_dict.get('sank_money_bf')

        if isinstance(orange_money_bf, dict):
            orange_money_bf = OperatorTransfBalanceData(**orange_money_bf)
        if isinstance(moov_money_bf, dict):
            orange_money_bf = OperatorTransfBalanceData(**moov_money_bf)
        if isinstance(sank_money_bf, dict):
            orange_money_bf = OperatorTransfBalanceData(**sank_money_bf)
        
        return cls(data_dict.get('total_available'), data_dict.get('total_pending'), orange_money_bf, moov_money_bf, sank_money_bf)

    def __post_init__(self):
        # Remove fields that are None
        if self.orange_money_bf is None:
            del self.__dict__['orange_money_bf']
        if self.moov_money_bf is None:
            del self.__dict__['moov_money_bf']
        if self.sank_money_bf is None:
            del self.__dict__['sank_money_bf']

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=8)

    def __repr__(self):
        return self.__str__()


@dataclass
class BalanceData:
    collection_balances: CollectionBalanceData
    transfer_balances: TransferBalanceData
    balance: float
    usable_balance: float
    currency: str

    @classmethod
    def from_dict(cls, data_dict):
        collection_balances = data_dict.get('collection_balances')
        transfer_balances = data_dict.get('transfer_balances')

        if isinstance(collection_balances, dict):
            collection_balances_obj = CollectionBalanceData(**collection_balances)
        else:
            collection_balances_obj = None
        
        if isinstance(transfer_balances, dict):
            transfer_balances_obj = TransferBalanceData.from_dict(transfer_balances)
        else:
            transfer_balances_obj = None
        
        return cls(collection_balances_obj, transfer_balances_obj, data_dict.get('balance'), data_dict.get('usable_balance'), data_dict.get('currency'))

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=8)

    def __repr__(self):
        return self.__str__()


@dataclass
class SenfenicoObject:
    status: bool
    message: str
    data: BalanceData
    error_code: Optional[str] = None
    errors: Optional[str] = None

    def __post_init__(self):
        # Remove fields that are None
        if self.error_code is None:
            del self.__dict__['error_code']
        if self.errors is None:
            del self.__dict__['errors']
        if self.data is None:
            del self.__dict__['data']
    
    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict.get('data')
        if isinstance(data, dict):
            #data_obj = BalanceData(**data)
            data_obj = BalanceData.from_dict(data)
        else:
            data_obj = None
        return cls(status=data_dict['status'], message=data_dict['message'], errors=data_dict.get('errors'), data=data_obj, error_code=data_dict.get('error_code'))

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=4)

    def __repr__(self):
        return self.__str__()


class Balance:

    @classmethod
    def fetch(cls) -> SenfenicoObject:
        from senfenico import api_key
        url = f"https://api.senfenico.com/v1/payment/balances"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-API-KEY': api_key
        }

        response = requests.get(url, headers=headers, data=payload)
        fetched_balance = SenfenicoObject.from_dict(response.json())
        return fetched_balance
