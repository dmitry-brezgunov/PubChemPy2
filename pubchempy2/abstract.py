from abc import ABC, abstractclassmethod
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

    @abstractclassmethod
    def _construct_input(self) -> str:
        pass

    @abstractclassmethod
    def _construct_operation(self) -> str:
        pass

    @abstractclassmethod
    def construct_search_request(self) -> dict[str, str]:
        pass
