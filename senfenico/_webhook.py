from dataclasses import dataclass
import requests
from typing import List, Optional, Union
from senfenico.utils import SenfenicoJSONEncoder
import json
import hashlib
from senfenico._settlement import SettlementData
from senfenico._checkout import CheckoutData
from senfenico._charge import ChargeData

@dataclass
class BalanceData:
    balance: float
    usable_balance: float
    currency: str

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=8)

    def __repr__(self):
        return self.__str__()


@dataclass
class SenfenicoObject:
    event: str
    data: Union[SettlementData, CheckoutData, ChargeData]

    @classmethod
    def from_dict(cls, data_dict):
        event = data_dict['event']
        data = data_dict.get('data')
        if event.split('.')[0] == 'charge':
            data_obj = ChargeData(**json.loads(data))
        elif event.split('.')[0] == 'checkout':
            data_obj = CheckoutData(**json.loads(data))
        elif event.split('.')[0] == 'settlement':
            data_obj = SettlementData(**json.loads(data))
        else:
            raise Exception('Unknown event')
        return cls(event=event, data=data_obj)

    def __str__(self):
        return json.dumps(self.__dict__, cls=SenfenicoJSONEncoder, indent=4)

    def __repr__(self):
        return self.__str__()


class Webhook:

    @classmethod
    def construct_event(cls, payload, webhook_hash, webhook_key) -> SenfenicoObject:
        if not isinstance(payload, dict):
            payload = json.loads(payload)

        payload_str = json.dumps(payload, sort_keys=False) + webhook_key

        computed_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        if webhook_hash != computed_hash:
            print('Hash mismatch, data might be tampered')
            raise ValueError('Hash mismatch, data might be tampered')

        return SenfenicoObject.from_dict(payload)
