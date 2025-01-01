from typing import Tuple, List
from pydantic import BaseModel, ConfigDict, Field
import uuid


class Element(BaseModel):
    """Base data class for all elements in the scene."""

    name: str
    location: Tuple[float, float, float]
    rotation: Tuple[float, float, float]
    scale: Tuple[float, float, float]
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Scene(BaseModel):
    """Base data class for all scenes."""

    name: str
    cameras: List[Element]
    axis: List[Element]
    elements: List[Element]
    lights: List[Element]
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Snapshot(BaseModel):
    """Base data class for all snapshots in a sweep."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    yaw: float
    roll: float
    camera_height: float
    light_energy: float


class Sweep(BaseModel):
    """Base data class for all sweeps."""

    name: str
    snapshots: List[Snapshot]
