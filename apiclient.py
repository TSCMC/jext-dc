import aiohttp
import aiohttp.web_exceptions
from typing import Optional

class jext_apiclient:
    def __init__(self, server: str, password: str):
        self.server: str = server.strip('/')
        self.__password: str = password
        self.__token: str = None
        self.__session: aiohttp.ClientSession = None

    async def __aenter__(self):
        await self.__session = aiohttp.ClientSession()
    
    async def __aexit__(self):
        await self.disconnect()
        self.__session.close()
    
    def _getEndpointUrl(self, endpoint: str) -> str:
        return self.server + endpoint
    
    def __getAuthHeader(self) -> dict:
        return {
            "Authorization": "Bearer " + self.__token
        }

    async def connect(self) -> bool:
        res = False

        async with self.__session.post(self._getEndpointUrl('/connect'), data=self.__password) as resp:
            if resp.status == 200:
                res = True
                self.__token = await resp.text()
        
        return res
    
    async def disconnect(self) -> None:
        async with self.__session.post(self._getEndpointUrl('/disconnect'), headers=self.__getAuthHeader()):
            pass
    
    async def get_discs_raw(self) -> bytes:
        async with self.__session.get(self._getEndpointUrl('/discs/read'), headers=self.__getAuthHeader()) as resp:
            res = await resp.read()
        
        return res

    async def apply_discs_raw(self, data: bytes) -> None:
        async with self.__session.post(self._getEndpointUrl('/discs/apply'), headers=self.__getAuthHeader(), data=data) as resp:
            pass
        
