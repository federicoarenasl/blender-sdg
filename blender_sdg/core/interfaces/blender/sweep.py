from blender_sdg.types.model import Sweep, Snapshot
from blender_sdg.config import SweepConfig
from itertools import product


class BlenderSweep(Sweep):
    """Interface for Blender sweeps."""

    def __init__(self, **kwargs):
        """Initialize the interface with a Blender sweep."""
        super().__init__(**kwargs)

    @classmethod
    def from_sweep_config(cls, sweep_config: SweepConfig):
        """Create a BlenderSweep object from an existing sweep."""
        return cls(
            name=sweep_config.sweep_name,
            snapshots=cls.snapshots_from_config(sweep_config),
        )

    @staticmethod
    def snapshots_from_config(sweep_config: SweepConfig) -> list[Snapshot]:
        """Generate snapshots from a sweep configuration."""
        # Collect yaw, roll, and camera height values
        yaw_range = range(
            int(sweep_config.yaw_limits[0]),
            int(sweep_config.yaw_limits[1]) + 1,
            sweep_config.step,
        )
        roll_range = range(
            int(sweep_config.roll_limits[0]),
            int(sweep_config.roll_limits[1]) + 1,
            sweep_config.step,
        )
        camera_height_range = range(
            int(sweep_config.camera_height_limits[0]),
            int(sweep_config.camera_height_limits[1]) + 1,
            sweep_config.step,
        )

        return [
            Snapshot(yaw, roll, camera_height)
            for yaw, roll, camera_height in product(
                yaw_range, roll_range, camera_height_range
            )
        ]
