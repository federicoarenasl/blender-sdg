from blender_sdg.core.interfaces.blender.scene import BlenderScene
from blender_sdg.core.interfaces.blender.sweep import BlenderSweep
from blender_sdg.core.interfaces.blender.object import BlenderElement
from blender_sdg.config import RenderingConfig
import bpy

from tqdm import tqdm
from typing import List, Tuple
import uuid
import warnings


class BlenderRenderer:
    """Interface for Blender rendering."""

    def __init__(self, scene: BlenderScene):
        """Initialize the interface with a Blender scene."""
        self.scene = scene

    @classmethod
    def from_scene(cls, scene: BlenderScene):
        """Create a BlenderRenderer object from an existing scene."""
        return cls(scene)

    def render_snapshot(
        self,
        resolution: Tuple[int, int],
        samples: int,
        output_path: str,
        snapshot_id: uuid.UUID,
    ):
        """Render a snapshot of the scene."""
        # Set the output path
        self.scene.blender_scene.render.filepath = f"{output_path}/{snapshot_id}.png"
        # Set the resolution
        self.scene.blender_scene.render.resolution_x = resolution[0]
        self.scene.blender_scene.render.resolution_y = resolution[1]
        # Take picture of current visible scene
        bpy.context.scene.cycles.samples = samples
        bpy.ops.render.render(write_still=True)

    def create_bounding_boxes(
        self,
        cameras: List[BlenderElement],
        elements: List[BlenderElement],
        file_path: str,
    ):
        """Create bounding boxes for the elements in the scene."""
        if len(cameras) > 1:
            warnings.warn(
                "Multiple cameras found in the scene. "
                "Bounding boxes will be created for the first camera only."
            )
        raise NotImplementedError


def render_sweep_from_config(config: RenderingConfig):
    """Render a sweep from a configuration."""
    # Initialize the scene, sweep, and renderer
    scene: BlenderScene = BlenderScene.from_scene_config(config.scene_config)
    sweep: BlenderSweep = BlenderSweep.from_sweep_config(config.sweep_config)
    renderer: BlenderRenderer = BlenderRenderer.from_scene(scene)

    # Render the sweep
    for snapshot in tqdm(sweep.snapshots, desc="Rendering snapshots"):
        # Prepare axis, camera and light
        scene.prepare_from_snapshot(snapshot=snapshot)
        # Render the snapshot, and create bounding boxes
        renderer.render_snapshot(
            resolution=config.resolution,
            samples=config.samples,
            output_path=config.target_path,
            snapshot_id=snapshot.id,
        )
        # Create bounding boxes
        renderer.create_bounding_boxes(
            cameras=scene.cameras,
            elements=scene.elements,
            file_path=config.target_path,
        )
