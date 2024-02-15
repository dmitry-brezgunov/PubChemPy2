from typing import Annotated, Literal, Optional, get_args

from pydantic import BaseModel, Field, model_validator

from .types import assay_types, compound_property_types, fast_search_types, output_types, xref_types, xrefs_types


class SubstanceSearch(BaseModel):
    domain: Literal["substance"] = "substance"
    namespace: Literal["sid", "sourceid", "sourceall", "name", "xref", "listkey"]
    sourceid: str = None
    xref: Optional[xref_types] = None
    identifiers: Annotated[list[str | int], Field(min_length=1)]
    operation: Literal["record", "synonyms", "sids", "cids", "aids", "assaysummary", "classification", "xrefs"] = (
        "record"
    )
    xrefs: Optional[list[xref_types | xrefs_types]] = None
    output: output_types

    @model_validator(mode="after")
    def check_sourceid(self) -> "SubstanceSearch":
        if self.namespace == "sourceid" and self.sourceid is None:
            raise ValueError("sourceid must be specified")
        if self.namespace != "sourceid" and self.sourceid:
            raise ValueError("sourceid must be None")
        return self

    @model_validator(mode="after")
    def check_xref(self) -> "SubstanceSearch":
        if self.namespace == "xref" and self.xref is None:
            raise ValueError("xref must be specified")
        if self.namespace != "xref" and self.xref:
            raise ValueError("xref must be None")
        return self

    @model_validator(mode="after")
    def check_xrefs(self) -> "SubstanceSearch":
        if self.operation == "xrefs" and self.xrefs is None:
            raise ValueError("xrefs must be specified")
        if self.operation != "xrefs" and self.xrefs:
            raise ValueError("xrefs must be None")
        return self


class CompoundSearch(BaseModel):
    domain: Literal["compound"] = "compound"
    namespace: (
        Literal["cid", "name", "smiles", "inchi", "sdf", "inchikey", "formula", "xref", "listkey"] | fast_search_types
    )
    fast_search: Optional[Literal["smiles", "smarts", "inchi", "sdf", "cid"]] = None
    xref: Optional[xref_types] = None
    identifiers: Annotated[list[str | int], Field(min_length=1)]
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
    output: output_types

    @model_validator(mode="after")
    def check_fast_search(self) -> "CompoundSearch":
        fast_search_args = get_args(fast_search_types)
        if self.namespace in fast_search_args and self.fast_search is None:
            raise ValueError("fast_search must be specified")
        if self.namespace not in fast_search_args and self.fast_search:
            raise ValueError("fast_search must be None")
        return self

    @model_validator(mode="after")
    def check_xref(self) -> "CompoundSearch":
        if self.namespace == "xref" and self.xref is None:
            raise ValueError("xref must be specified")
        if self.namespace != "xref" and self.xref:
            raise ValueError("xref must be None")
        return self

    @model_validator(mode="after")
    def check_compound_property(self) -> "CompoundSearch":
        if self.operation == "property" and self.compound_property is None:
            raise ValueError("compound_property must be specified")
        if self.operation != "property" and self.compound_property:
            raise ValueError("compound_property must be None")
        return self

    @model_validator(mode="after")
    def check_xrefs(self) -> "CompoundSearch":
        if self.operation == "xrefs" and self.xrefs is None:
            raise ValueError("xrefs must be specified")
        if self.operation != "xrefs" and self.xrefs:
            raise ValueError("xrefs must be None")
        return self


class AssaySearch(BaseModel):
    domain: Literal["assay"] = "assay"
    namespace: Literal["aid", "listkey", "type", "sourceall", "target", "activity"]
    target: Optional[Literal["gi", "proteinname", "geneid", "genesymbol", "accession"]] = None
    identifiers: Annotated[list[str | int], Field(min_length=1)]
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
    output: output_types

    @model_validator(mode="after")
    def check_type(self) -> "AssaySearch":
        assay_types_args = get_args(assay_types)
        if self.namespace == "type" and len(self.identifiers) != 1:
            raise ValueError("identifiers must have exactly one value")
        if self.namespace == "type" and self.identifiers[0] not in assay_types_args:
            raise ValueError(f"identifiers must be one of following: {assay_types_args}")
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