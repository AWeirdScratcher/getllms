import gzip
import importlib
import json
import os
from typing import List, Literal, Union, overload

import requests

from .model import Model

__here = os.path.dirname(__file__)
__savefile = os.path.join(__here, "data.py")

def download_model_data() -> None:
    """Download the latest model data.

    Downloaded contents will be cached and compressed.

    Import downloaded data (raw):

    .. code-block :: python

        from getllms.data import RAW
        print(RAW) # b'…'

    .. info ::

        The downloaded data is compressed using ``gzip``.
        After decompressing, the raw JSON data would be present.
    """
    r = requests.get(
        "https://raw.githubusercontent.com/lmstudio-ai/model-catalog/main/catalog.json"
    )

    r.raise_for_status()

    with open(__savefile, "wb") as f:
        f.write(
            b"RAW=" + 
            f"{gzip.compress(r.content)!r}".encode('utf-8') +
            b" # noqa: E501"
        )


def erase_data(*, reload: bool=True) -> None:
    """Erase all the cached model data.

    Args:
        reload (bool): Reload ``getllms.data``?
    """
    with open(__savefile, "wb") as f:
        f.write(b"RAW=b''")

    if reload:
        from . import data as dataf
        importlib.reload(dataf)


def read_data() -> bytes:
    """Read the data from cache.

    Returns:
        bytes: Decompressed raw JSON.
    """
    from . import data as dataf

    raw = dataf.RAW

    if not raw:
        download_model_data()
        raw = importlib.reload(dataf).RAW

    return gzip.decompress(raw)

@overload
def list_models(*, raw: Literal[False] = False) -> List[Model]: ...

@overload
def list_models(*, raw: Literal[True] = True) -> List[list]: ...

def list_models(*, raw=False) -> Union[List[Model], List[list]]:
    """List all models.

    Args:
       raw (bool): Whether to return the raw data instead of dataclasses. 
    """
    data: list = json.loads(read_data())

    return [Model(model) for model in data] if not raw else data

def get_model(name: str) -> Model:
    """Get a model.
    
    Args:
        name (str): Model name.
    """
    m = { model.name: model for model in list_models() }

    return m[name]
