from typing import List, Tuple
from pydantic import BaseModel, Field
from enum import Enum
from itertools import product


class SupportedEngines(str, Enum):
    """Supported rendering engines."""

    BLENDER = "blender"


class SceneConfig(BaseModel):
    scene_name: str
    scene_path: str
    camera_names: List[str]
    axis_names: List[str]
    element_names: List[str]
    light_names: List[str]


class SnapshotConfig(BaseModel):
    yaw: int
    roll: int
    camera_height: int


class SweepConfig(BaseModel):
    step: int
    yaw_limits: Tuple[float, float]
    roll_limits: Tuple[float, float]
    camera_height_limits: Tuple[float, float]
    random_seed: int
    snapshots: List[SnapshotConfig] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self.generate_snapshots()

    def generate_snapshots(self):
        yaw_range = range(
            int(self.yaw_limits[0]), int(self.yaw_limits[1]) + 1, self.step
        )
        roll_range = range(
            int(self.roll_limits[0]), int(self.roll_limits[1]) + 1, self.step
        )
        camera_height_range = range(
            int(self.camera_height_limits[0]),
            int(self.camera_height_limits[1]) + 1,
            self.step,
        )

        self.snapshots = [
            SnapshotConfig(yaw, roll, camera_height)
            for yaw, roll, camera_height in product(
                yaw_range, roll_range, camera_height_range
            )
        ]


class RenderingConfig(BaseModel):
    target_path: str
    engine: SupportedEngines
    scene_config: SceneConfig
    sweep_config: SweepConfig


def config_from_yaml(yaml_config: dict) -> RenderingConfig:
    """Create a rendering configuration from a YAML file."""
    return RenderingConfig(**yaml_config)
