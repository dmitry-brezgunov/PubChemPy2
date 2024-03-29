from abc import ABC, abstractclassmethod
from typing import Annotated, ClassVar

import requests
from pydantic import BaseModel, Field, HttpUrl
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_fixed

from .errors import SeverBusyError, handle_http_error
from .literals import output_types


class SearchParams(BaseModel):
    uri: HttpUrl
    body: dict[str, str]


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
    def _construct_search_request(self) -> SearchParams:
        pass

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), retry=retry_if_exception(SeverBusyError))
    def search(self) -> requests.Response:
        search_request = self._construct_search_request()
        response = requests.post(url=search_request.uri, data=search_request.body)

        if not response.ok:
            handle_http_error(response)

        return response
