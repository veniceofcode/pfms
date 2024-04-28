import  os
from    typing              import Any
from    pydantic            import AnyHttpUrl, AnyUrl
from    pydantic_settings   import BaseSettings
from    pftag               import pftag


class Vault(BaseSettings):
    locked:bool             = False
    vaultKey:str            = ''

class Credentials(BaseSettings):
    username:str            = 'chris'
    password:str            = 'chris1234'

def vaultCheckLock(vault:Vault) -> None:
    if vault.vaultKey and not vault.locked:
        vault.locked        = True
        print("Vault check: key has already been set. Vault is now LOCKED.")

vault               = Vault()
