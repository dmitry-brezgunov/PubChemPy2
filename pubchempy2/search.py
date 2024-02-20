from typing import Literal, Optional
from urllib.parse import quote

from pydantic import model_validator

from .abstract import AbstractSearch, SearchParams
from .literals import assay_types, compound_property_types, fast_search_args, fast_search_types, xref_types, xrefs_types
from .validators import XrefValidators


class SubstanceSearch(AbstractSearch, XrefValidators):
    domain: Literal["substance"] = "substance"
    namespace: Literal["sid", "sourceid", "sourceall", "name", "xref", "listkey"]
    sourceid: str = None
    xref: Optional[xref_types] = None
    operation: Literal["record", "synonyms", "sids", "cids", "aids", "assaysummary", "classification", "xrefs"] = (
        "record"
    )
    xrefs: Optional[list[xref_types | xrefs_types]] = None

    @model_validator(mode="after")
    def check_sourceid(self) -> "SubstanceSearch":
        if self.namespace == "sourceid" and self.sourceid is None:
            raise ValueError("sourceid must be specified")
        if self.namespace != "sourceid" and self.sourceid:
            raise ValueError("sourceid must be None")
        return self

    def _construct_input(self) -> str:
        input_part = f"{self.domain}/{self.namespace}"

        if self.namespace == "sourceid":
            input_part += f"/{quote(self.sourceid).replace('/', '.')}"
        if self.namespace == "sourceall":
            input_part += f"/{quote(str(self.identifiers[0])).replace('/', '.')}"
        if self.namespace == "xref":
            input_part += f"/{self.xref}/{str(self.identifiers[0])}"
        if self.namespace == "listkey":
            input_part += f"/{str(self.identifiers[0])}"

        return input_part

    def _construct_operation(self) -> str:
        operation_part = f"{self.operation}"

        if self.operation == "xrefs":
            operation_part += f"/{','.join(self.xrefs)}"

        return operation_part

    def _construct_search_request(self) -> SearchParams:
        input_part = self._construct_input()
        operation_part = self._construct_operation()
        uri = f"{self.prolog}/{input_part}/{operation_part}/{self.output}"
        body = {}

        if self.namespace not in ("sourceall", "xref", "listkey"):
            body |= {self.namespace: ",".join([str(val) for val in self.identifiers])}

        return SearchParams(uri=uri, body=body)


class CompoundSearch(AbstractSearch, XrefValidators):
    domain: Literal["compound"] = "compound"
    namespace: (
        Literal["cid", "name", "smiles", "inchi", "inchikey", "fastformula", "xref", "listkey"] | fast_search_types
    )
    fast_search: Optional[Literal["smiles", "smarts", "inchi", "cid"]] = None
    xref: Optional[xref_types] = None
    operation: Literal[
        "record",
        "property",
        "synonyms",
        "sids",
        "cids",
        "aids",
        "assaysummary",
        "classification",
        "xrefs",
        "description",
        "conformers",
    ] = "record"
    compound_property: Optional[list[compound_property_types]] = None
    xrefs: Optional[list[xref_types | xrefs_types]] = None

    @model_validator(mode="after")
    def check_fast_search(self) -> "CompoundSearch":
        if self.namespace in fast_search_args and self.fast_search is None:
            raise ValueError("fast_search must be specified")
        if self.namespace not in fast_search_args and self.fast_search:
            raise ValueError("fast_search must be None")
        return self

    @model_validator(mode="after")
    def check_compound_property(self) -> "CompoundSearch":
        if self.operation == "property" and not self.compound_property:
            raise ValueError("compound_property must be specified")
        if self.operation != "property" and self.compound_property:
            raise ValueError("compound_property must be None")
        return self

    def _construct_input(self) -> str:
        input_part = f"{self.domain}/{self.namespace}"

        if self.namespace == "xref":
            input_part += f"/{self.xref}/{str(self.identifiers[0])}"
        if self.namespace == "listkey" or self.fast_search == "cid":
            input_part += f"/{str(self.identifiers[0])}"
        if self.namespace == "fastformula":
            input_part += f"/{quote(','.join(self.identifiers))}"
        if self.namespace in fast_search_args:
            input_part += f"/{self.fast_search}"

        return input_part

    def _construct_operation(self) -> str:
        operation_part = f"{self.operation}"

        if self.operation == "property":
            operation_part += f"/{','.join(self.compound_property)}"
        if self.operation == "xrefs":
            operation_part += f"/{','.join(self.xrefs)}"

        return operation_part

    def _construct_search_request(self) -> SearchParams:
        input_part = self._construct_input()
        operation_part = self._construct_operation()
        uri = f"{self.prolog}/{input_part}/{operation_part}/{self.output}"
        body = {}

        if self.namespace not in ("xref", "listkey", "fastformula", *fast_search_args):
            body |= {self.namespace: ",".join([str(val) for val in self.identifiers])}
        if self.namespace in fast_search_args and self.fast_search != "cid":
            body |= {self.fast_search: ",".join([str(val) for val in self.identifiers])}
        if self.namespace == "inchi":
            body[self.namespace] = f"InChI={body[self.namespace]}"
        if self.fast_search == "inchi":
            body[self.fast_search] = f"InChI={body[self.fast_search]}"

        return SearchParams(uri=uri, body=body)


class AssaySearch(AbstractSearch):
    domain: Literal["assay"] = "assay"
    namespace: Literal["aid", "listkey", "type", "sourceall", "target", "activity"]
    target: Optional[Literal["gi", "proteinname", "geneid", "genesymbol", "accession"]] = None
    operation: Literal[
        "record",
        "concise",
        "aids",
        "sids",
        "cids",
        "description",
        "targets",
        "doseresponse",
        "summary",
        "classification",
    ] = "record"
    targets: Optional[list[Literal["ProteinGI", "ProteinName", "GeneID", "GeneSymbol"]]] = None

    @model_validator(mode="after")
    def check_type(self) -> "AssaySearch":
        if self.namespace == "type" and len(self.identifiers) != 1:
            raise ValueError("identifiers must have exactly one value")
        if self.namespace == "type" and self.identifiers[0] not in assay_types:
            raise ValueError(f"identifiers must be one of following: {assay_types}")
        return self

    @model_validator(mode="after")
    def check_target(self) -> "AssaySearch":
        if self.namespace == "target" and self.target is None:
            raise ValueError("target must be specified")
        if self.namespace != "target" and self.target:
            raise ValueError("target must be None")
        return self

    @model_validator(mode="after")
    def check_targets(self) -> "AssaySearch":
        if self.operation == "targets" and not self.targets:
            raise ValueError("targets must be specified")
        if self.operation != "targets" and self.targets:
            raise ValueError("targets must be None")
        return self

    def _construct_input(self) -> str:
        input_part = f"{self.domain}/{self.namespace}"

        if self.namespace in ("listkey", "type"):
            input_part += f"/{str(self.identifiers[0])}"
        if self.namespace in ("sourceall", "activity"):
            input_part += f"/{quote(str(self.identifiers[0])).replace('/', '.')}"
        if self.namespace == "target":
            input_part += f"/{self.target}"

        return input_part

    def _construct_operation(self) -> str:
        operation_part = f"{self.operation}"
        if self.operation == "targets":
            operation_part += f"/{','.join(self.targets)}"
        return operation_part

    def _construct_search_request(self) -> SearchParams:
        input_part = self._construct_input()
        operation_part = self._construct_operation()
        uri = f"{self.prolog}/{input_part}/{operation_part}/{self.output}"
        body = {}

        if self.namespace == "aid":
            body |= {self.namespace: ",".join([str(val) for val in self.identifiers])}
        if self.namespace == "target":
            body |= {self.target: str(self.identifiers[0])}

        return SearchParams(uri=uri, body=body)
