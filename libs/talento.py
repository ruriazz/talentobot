import aiohttp
import pytz
from datetime import datetime
from typing import Dict, Any, Union, Optional, Tuple, List
from pydantic import BaseModel, Field
from bot.settings import TALENTO_API_URL


class TalentoUser(BaseModel):
    uid: str
    fullname: str = Field(alias='fullName')
    email: str

class TalentoAuthResult(BaseModel):
    user: TalentoUser
    auth_token: str
    refresh_token: str


class Talento:
    authorization: Dict[str, Any]
    def __init__(self, auth_token: Optional[str] = '') -> None:
        self.authorization = {}

        if auth_token:
            self.authorization = {'Authorization': f"Bearer {auth_token}"}

    @staticmethod
    def _rest_url(path: str) -> str:
        return f"{TALENTO_API_URL}{path}"

    async def authentication(self, email: str, password: str, force_compile: bool = False) -> Union[str, TalentoAuthResult]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                        self._rest_url('/talenta/account/auth'),
                        json={ 'email': email, 'password': password }
                    ) as resp:
                resp_json = await resp.json()
                if resp.status == 200:
                    data = resp_json['data']
                    return TalentoAuthResult(user=TalentoUser(**data['talentaAccount']), auth_token=data['authToken'], refresh_token=data['refreshToken'])

                return None if force_compile else resp_json['message']

    async def create_attendance(self, attendance_type: str) -> Tuple[bool, str]:
        async with aiohttp.ClientSession() as session:
            async with session.post(self._rest_url(f'/talenta/attendance/{attendance_type}'), headers=self.authorization) as resp:
                resp_json = await resp.json()
                if resp.status == 200:
                    return True, resp_json['data']['token']
                
                return False, resp_json['message']
            
    async def submit_attendance(self, token: str) -> Union[str, Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            async with session.put(self._rest_url('/talenta/attendance'), json={ 'token': token }, headers=self.authorization) as resp:
                resp_json = await resp.json()
                if resp.status == 200:
                    return True, resp_json['data']

                return False, resp_json['message']

    async def get_histories(self, date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        date = date or datetime.now().replace(tzinfo=pytz.timezone('Asia/Jakarta'))
        async with aiohttp.ClientSession() as session:
            async with session.get(self._rest_url(f'/talenta/attendance/{date.strftime("%Y-%m-%d")}'), headers=self.authorization) as resp:
                if resp.status == 200:
                    resp_json = await resp.json()
                    return resp_json['data']
        return []