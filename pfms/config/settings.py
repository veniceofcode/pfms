import os
from typing import Any
from pydantic import AnyHttpUrl, AnyUrl
from pydantic_settings import BaseSettings
from pftag import pftag
from pathlib import Path


class ModelMeta(BaseSettings):
    location: Path = Path.home() / "spleenseg" / "models"
    device: str = "cuda:0"


class AnalysisMeta(BaseSettings):
    location: Path = Path.home() / "spleenseg" / "analysis"


class Vault(BaseSettings):
    locked: bool = False
    vaultKey: str = ""


class Credentials(BaseSettings):
    username: str = "chris"
    password: str = "chris1234"


def vaultCheckLock(vault: Vault) -> None:
    if vault.vaultKey and not vault.locked:
        vault.locked = True
        print("Vault check: key has already been set. Vault is now LOCKED.")


vault = Vault()
modelMeta = ModelMeta()

analysisMeta = AnalysisMeta()
# analysisMeta.location.mkdir(parents=True, exist_ok=True)
