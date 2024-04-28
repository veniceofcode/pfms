from fastapi import APIRouter, Query, HTTPException, BackgroundTasks, Request
from fastapi import File, UploadFile
from typing import List, Dict, Any, Union

from models import credentialModel
from models import iresponse
from controllers import pfmsController_inference
from routes import credentialRouter

from config import settings
from pftag import pftag
import pudb

router = APIRouter()
router.tags = ["pfms endpoints"]


@router.get(
    "/spleenseg/models/",
    response_model=iresponse.modelsAvailable,
    summary="""
    GET the list of available models.
    """,
)
def models_listAll() -> iresponse.modelsAvailable:
    """
    Description
    -----------

    GET the current list of models in the pfms server.

    Returns
    -------
    * `iresponse.modelsAvailable`: The response containing the list of models
    """
    # pudb.set_trace()
    modelList: iresponse.modelsAvailable = pfmsController_inference.showAll()
    return modelList


@router.post(
    "/spleenseg/NIfTIinference/",
    response_model=iresponse.inferenceResponseNIFTI,
    summary="""
        POST a NIfTI volume and expect an inference.
          """,
)
async def uploadAndInferOnNIfTIfile(
    file: UploadFile = File(...),
) -> iresponse.inferenceResponseNIFTI:
    """
    Description
    -----------

    POST a NIfTI volume spleen scan, and expect a reponse inference.

    Returns
    -------
    * `iresponse.inferenceResponseNIFTI`: The response containing the list of models
    """
    pudb.set_trace()
    inference: iresponse.inferenceResponseNIFTI = (
        await pfmsController_inference.inferenceOnNIfTI(file)
    )

    return inference
