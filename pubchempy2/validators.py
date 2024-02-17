from typing import Protocol

from pydantic import model_validator

from .abstract import AbstractSearch


class XrefProto(Protocol):
    namespace: str
    xref: str
    operation: str
    xrefs: list[str]


class XrefValidators:
    @model_validator(mode="after")
    def check_xref(self: XrefProto) -> "AbstractSearch":
        if self.namespace == "xref" and self.xref is None:
            raise ValueError("xref must be specified")
        if self.namespace != "xref" and self.xref:
            raise ValueError("xref must be None")
        return self

    @model_validator(mode="after")
    def check_xrefs(self: XrefProto) -> "AbstractSearch":
        if self.operation == "xrefs" and not self.xrefs:
            raise ValueError("xrefs must be specified")
        if self.operation != "xrefs" and self.xrefs:
            raise ValueError("xrefs must be None")
        return self
