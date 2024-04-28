from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel
import pudb
from config import settings


class inferenceResponseNIFTI(BaseModel):
    inputfilename: str = ""
    shape: list[int] = []
    dtype: str = ""
    data: list[float] = []


class modelsAvailable(BaseModel):
    models: list[str] = []
