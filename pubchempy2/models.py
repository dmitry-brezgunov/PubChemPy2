from typing import Optional

from pydantic import BaseModel


class Element(BaseModel):
    atomic_number: int
    symbol: str
    name: str
    atomic_mass: float
    cpkhex_color: Optional[str]
    electron_configuration: str
    electro_negativity: Optional[float]
    atomic_radius: Optional[int]
    ionization_energy: Optional[float]
    electron_affinity: Optional[float]
    oxidation_states: list[int]
    standard_state: str
    melting_point: Optional[float]
    boiling_point: Optional[float]
    density: Optional[float]
    group_block: str
    year_discovered: str


class Atom(BaseModel):
    aid: int
    element: Element
    x_coord: float
    y_coord: float
    z_coord: Optional[float]
    coord_type: str
    coord_calc: str
    coord_units: str
