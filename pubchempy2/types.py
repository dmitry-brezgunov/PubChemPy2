from typing import Literal

fast_search_types = Literal[
    "fastidentity", "fastsimilarity_2d", "fastsimilarity_3d", "fastsubstructure", "fastsuperstructure", "fastformula"
]

compound_property_types = Literal[
    "MolecularFormula",
    "MolecularWeight",
    "CanonicalSMILES",
    "IsomericSMILES",
    "InChI",
    "InChIKey",
    "IUPACName",
    "Title",
    "XLogP",
    "ExactMass",
    "MonoisotopicMass",
    "TPSA",
    "Complexity",
    "Charge",
    "HBondDonorCount",
    "HBondAcceptorCount",
    "RotatableBondCount",
    "HeavyAtomCount",
    "IsotopeAtomCount",
    "AtomStereoCount",
    "DefinedAtomStereoCount",
    "UndefinedAtomStereoCount",
    "BondStereoCount",
    "DefinedBondStereoCount",
    "UndefinedBondStereoCount",
    "CovalentUnitCount",
    "PatentCount",
    "PatentFamilyCount",
    "LiteratureCount",
    "Volume3D",
    "XStericQuadrupole3D",
    "YStericQuadrupole3D",
    "ZStericQuadrupole3D",
    "FeatureCount3D",
    "FeatureAcceptorCount3D",
    "FeatureDonorCount3D",
    "FeatureAnionCount3D",
    "FeatureCationCount3D",
    "FeatureRingCount3D",
    "FeatureHydrophobeCount3D",
    "ConformerModelRMSD3D",
    "EffectiveRotorCount3D",
    "ConformerCount3D",
    "Fingerprint2D",
]

xref_types = Literal[
    "RegistryID",
    "RN",
    "PubMedID",
    "MMDBID",
    "ProteinGI",
    "NucleotideGI",
    "TaxonomyID",
    "MIMID",
    "GeneID",
    "ProbeID",
    "PatentID",
]

xrefs_types = Literal["DBURL", "SBURL", "SourceName", "SourceCategory"]

assay_types = Literal[
    "all",
    "confirmatory",
    "doseresponse",
    "onhold",
    "panel",
    "rnai",
    "screening",
    "summary",
    "cellbased",
    "biochemical",
    "invivo",
    "invitro",
    "activeconcentrationspecified",
]

output_types = Literal["XML", "ASNT", "ASNB", "JSON", "JSONP", "SDF", "CSV", "PNG", "TXT"]
