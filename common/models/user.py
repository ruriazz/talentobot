import json
from secrets import token_urlsafe
from typing import Optional
from pydantic import BaseModel as _BaseModel, Field
from common.database import BaseModel
from datetime import datetime
import peewee as pw

from libs.text_encryption import TextEncryption

class _AuthData(_BaseModel):
    username: str = Field(init=False, default=None)
    password: str = Field(init=False, default=None)
    auth_token: Optional[str] = Field(init=False, default=None)

    def __eq__(self, other: "_AuthData") -> bool:
        if isinstance(other, _AuthData):
            return self.username == other.username \
                and self.password == other.password \
                and self.auth_token == other.auth_token

        return False


class User(BaseModel):
    class Meta:
        table_name = 'users'

    id = pw.AutoField(primary_key=True)
    uid = pw.BigIntegerField()
    private_key = pw.TextField()
    auth_data = pw.TextField()
    created_at = pw.DateTimeField(default=datetime.now)

    @property
    def PrivateKey(self) -> str:
        if not self.private_key:
            return token_urlsafe(56)

        try:
            return self.TextEncryption() \
                .decrypt(self.private_key)
        except Exception as err:
            self.Log().warning(f"User.PrivateKey Exception: {err}")

    @property
    def AuthData(self) -> _AuthData:
        if auth_data := self.auth_data:
            auth_data = self.Decrypt(auth_data)
            return _AuthData(**json.loads(auth_data))
        return _AuthData()

    def Encrypt(self, plaintext: str) -> str:
        enc = self.TextEncryption(self.PrivateKey if self.private_key else None)
        return enc.encrypt(plaintext)

    def Decrypt(self, ciphertext_b64: str) -> str:
        enc = self.TextEncryption(self.PrivateKey if self.private_key else None)
        return enc.decrypt(ciphertext_b64)

    @staticmethod
    def Create(uid: int) -> Optional["User"]:
        try:
            with User.Atomic():
                privkey = User.TextEncryption().encrypt(
                    User().PrivateKey
                )
                result = User.create(uid=uid, private_key=privkey)
            return result
        except Exception as err:
            User.Log().warning(f"User.Create Exception: {err}")

    def UpdateAuthData(self, username: str | None = None, password: str | None = None, auth_token: str | None = None) -> "User":
        auth_data = self.AuthData
        auth_data.username = username or auth_data.username
        auth_data.password = password or auth_data.password
        auth_data.auth_token = auth_token or auth_data.auth_token

        if auth_data != self.AuthData:
            with self.Atomic():
                encrypted_data = self.Encrypt(auth_data.model_dump_json())
                if _ := User.update(auth_data=encrypted_data) \
                    .where(User.id==self.id) \
                    .execute():
                    self.auth_data = encrypted_data
        return self