"""
test_assay
~~~~~~~~~~

Test assay object.

"""

import pytest

from pubchempy2.pubchempy import Assay, ProjectCategory, text_types


@pytest.fixture(scope="module")
def a1():
    """Assay AID 1000."""
    return Assay.from_aid(1000)


def test_basic(a1):
    assert a1.aid == 1000
    assert repr(a1) == "Assay(1000)"
    assert a1.record


def test_meta(a1):
    assert isinstance(a1.name, text_types)
    assert a1.project_category == ProjectCategory.MLSCN
    assert isinstance(a1.description, list)
    assert isinstance(a1.comments, list)


def test_assay_equality():
    first = Assay.from_aid(1000)
    second = Assay.from_aid(1001)
    assert first == first
    assert second == second
    assert first != second


def test_assay_dict(a1):
    assert isinstance(a1.to_dict(), dict)
    assert a1.to_dict()
