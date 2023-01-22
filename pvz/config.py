from pydantic import BaseModel, Extra
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
    pvz_path: Path = Path()