from fastapi import APIRouter, Query, Request
from fastapi import File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Callable, Any

import asyncio
from models import iresponse
import os
from datetime import datetime

import json
import pudb
from config import settings

from argparse import Namespace, ArgumentParser
import sys
from loguru import logger
import shutil

import tempfile
from pathlib import Path
import uuid
from uuid import UUID

from spleenseg import spleenseg as spleen
from spleenseg import splparser as psr

LOG = logger.debug

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> │ "
    "<level>{level: <5}</level> │ "
    "<yellow>{name: >28}</yellow>::"
    "<cyan>{function: <30}</cyan> @"
    "<cyan>{line: <4}</cyan> ║ "
    "<level>{message}</level>"
)
logger.remove()
logger.opt(colors=True)
logger.add(sys.stderr, format=logger_format)
LOG = logger.info


def noop():
    """
    A dummy function that does nothing.
    """
    return {"status": True}


def showAll() -> iresponse.modelsAvailable:
    resp: iresponse.modelsAvailable = iresponse.modelsAvailable()
    resp.models = ["spleensegmentation.pth"]
    return resp


def IOpaths_create() -> tuple[Path, Path]:
    sessionUUID: UUID = uuid.uuid4()
    baseParentPath: Path = Path(
        Path(tempfile.mkdtemp()) / "imagesTs" / str(sessionUUID)
    )
    inputDir: Path = baseParentPath / "input"
    outputDir: Path = baseParentPath / "output"
    inputDir.mkdir(parents=True, exist_ok=True)
    outputDir.mkdir(parents=True, exist_ok=True)
    return inputDir, outputDir


def NIfTIvol_save(remote: File, inputDir: Path) -> Path:
    savePath: Path = inputDir / "input.nii.gz"
    with savePath.open("wb") as buffer:
        shutil.copyfileobj(remote.file, buffer)
    return savePath


def NIfTIvol_infer(remote: File) -> Path:
    inputDir: Path
    outputDir: Path
    inputDir, outputDir = IOpaths_create()
    NIfTIvol_save(remote, inputDir)
    options: Namespace = psr.parser_interpret(psr.parser_setup(""))
    options.mode = "inference"
    spleen.main(options, inputDir, outputDir)
    return outputDir


async def inferenceOnNIfTI(uploadFile: File) -> iresponse.inferenceResponseNIFTI:
    iresp: iresponse.inferenceResponseNIFTI = iresponse.inferenceResponseNIFTI()
    result: Path = NIfTIvol_infer(uploadFile)
    return iresp
