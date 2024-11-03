from typing import Tuple, List
from pydantic import BaseModel


class Element(BaseModel):
    """Base data class for all elements in the scene."""

    name: str
    location: Tuple[float, float, float]
    rotation: Tuple[float, float, float]
    scale: Tuple[float, float, float]


class Scene(BaseModel):
    """Base data class for all scenes."""

    name: str
    cameras: List[Element]
    axis: List[Element]
    elements: List[Element]
    lights: List[Element]


class Snapshot(BaseModel):
    """Base data class for all snapshots in a sweep."""

    yaw: int
    roll: int
    camera_height: int


class Sweep(BaseModel):
    """Base data class for all sweeps."""

    name: str
    snapshots: List[Snapshot]
