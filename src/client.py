import asyncio
from enum import Enum
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, PhoneCodeExpiredError
from config import CLIENT_API_HASH, CLIENT_API_ID


class ClientResult(Enum):
    LOGIN_SUCCESS = 0
    SEND_CODE_SUCCESS = 1
    INVALID_CODE = 2
    CODE_EXPIRED = 3
    SOME_ERROR = 4


class Client:
    def __init__(self, phone='') -> None:
        self._phone = phone
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._client = TelegramClient(
            phone, 
            CLIENT_API_ID, 
            CLIENT_API_HASH, 
            loop=loop
        )
        self._client.connect()
    
    @property
    def is_authorized(self) -> bool:
        return bool(self._client.is_user_authorized())
    
    def authorization(self):
        try:
            self._client.send_code_request(self._phone)
        except Exception as e:
            print(e)
            self._client.session.delete()
            return ClientResult.SOME_ERROR
        # self._client.send_code_request(self._phone)
        return ClientResult.SEND_CODE_SUCCESS
    
    def set_code(self, code) -> int:
        try:
            self._client.sign_in(self._phone, code)
        except PhoneCodeInvalidError:
            self._client.session.delete()
            return ClientResult.INVALID_CODE
        except PhoneCodeExpiredError:
            self._client.session.delete()
            return ClientResult.CODE_EXPIRED
        except Exception as e:
            print(e)
            self._client.session.delete()
            return ClientResult.SOME_ERROR
        return ClientResult.LOGIN_SUCCESS
    
    @property
    def all_sessions(self) -> list:
        return self._client.session.list_sessions()


# client = Client('+9967069922656')
# print(Client().all_sessions)



# client = TelegramClient('', CLIENT_API_ID, CLIENT_API_HASH)
# client.connect()
# print(client.is_user_authorized())
# print(client.session.list_sessions())
# if not client.is_user_authorized():
#     print(client.send_code_request('+996706992265678'))
#     try:
#         print(client.sign_in('+996706992265678', input()))
#     except PhoneCodeInvalidError:
#         print('invalid code')
#     except PhoneCodeExpiredError:
#         print('code is expired')
#     except:
#         print()
#     else:
#         print(client.is_user_authorized())
# else: print('hello')
# print(client.session.close())