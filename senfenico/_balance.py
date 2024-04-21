from dataclasses import dataclass
import requests
from typing import List, Optional


@dataclass
class BalanceData:
    balance: float
    usable_balance: float
    currency: str

    def __str__(self):
        return f'''{{
            \t\t"balance": {self.balance},
            \t\t"usable_balance": {self.usable_balance},
            \t\t"currency": {self.currency},
            \n\t}}'''

    def __repr__(self):
        return self.__str__()


@dataclass
class SenfenicoObject:
    status: bool
    message: str
    data: BalanceData
    errors: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        data = data_dict.get('data')
        if isinstance(data, dict):
            data_obj = BalanceData(**data)
        else:
            data_obj = None
        return cls(status=data_dict['status'], message=data_dict['message'], errors=data_dict.get('errors'), data=data_obj)

    def __str__(self):
        return f'{{\n\t"status": {self.status},\n\t"message": {self.message},\n\t"errors": {self.errors},\n\t"data": {self.data}\n}}'

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
