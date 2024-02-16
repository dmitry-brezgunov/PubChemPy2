from abc import ABC
from typing import Annotated, ClassVar

from pydantic import BaseModel, Field

from .types import output_types


class AbstractSearch(BaseModel, ABC):
    prolog: ClassVar[str] = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    domain: str
    namespace: str
    identifiers: Annotated[list[str | int], Field(min_length=1)]
    operation: str
    output: output_types
