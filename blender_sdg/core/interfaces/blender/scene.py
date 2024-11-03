"""Blender scene interface for the SDG."""

import bpy
from blender_sdg.core.model import Scene, Snapshot
from blender_sdg.config import SceneConfig
from blender_sdg.core.interfaces.blender.object import BlenderElement


class BlenderScene(Scene):
    """Interface for Blender scenes."""

    def __init__(
        self,
        blender_scene: bpy.types.Scene,
        **kwargs,
    ):
        """Initialize the interface with a Blender scene."""
        self.blender_scene = blender_scene
        super().__init__(**kwargs)

    def prepare_from_snapshot(self, snapshot: Snapshot):
        """Prepare the scene for a snapshot."""
        # Prepare axis, camera and light
        self.axis.set_location((0, 0, 0))
        self.axis.set_rotation((snapshot.yaw, snapshot.roll, 0))
        self.camera.set_location((0, 0, snapshot.camera_height))
        self.light.set_energy(snapshot.light_energy)

    @classmethod
    def from_scene_config(
        cls,
        scene_config: SceneConfig,
    ):
        """Create a BlenderScene object from an existing scene."""
        # Load the scene from the file path
        cls._load_from_scene_path(scene_config.scene_path)

        # Map the scene configuration to the Blender objects
        config_map = {
            "cameras": scene_config.camera_name,
            "axis": scene_config.axis_name,
            "elements": scene_config.element_names,
            "lights": scene_config.light_names,
        }

        # Initialize and populate the attributes
        attributes = {
            "name": scene_config.scene_name,
            "blender_scene": bpy.data.scenes[scene_config.scene_name],
        }
        for attr, config_name in config_map.items():
            attributes[attr] = cls._get_blender_objects(config_name)

        return cls(**attributes)

    @staticmethod
    def _get_blender_objects(names: list[str]) -> list[BlenderElement]:
        return [
            BlenderElement.from_bpy_object(bpy.data.objects[name]) for name in names
        ]

    @staticmethod
    def _load_from_scene_path(scene_path: str) -> bpy.types.Scene:
        bpy.ops.wm.open_mainfile(filepath=scene_path)
