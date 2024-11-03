from blender_sdg.core.interfaces.blender.scene import BlenderScene
from blender_sdg.core.interfaces.blender.sweep import BlenderSweep
from blender_sdg.core.interfaces.blender.object import BlenderElement
from blender_sdg.config import RenderingConfig
from blender_sdg.core.model import Snapshot
import bpy

from tqdm import tqdm
from typing import List

SCENE_SAMPLES = 128


class BlenderRenderer:
    """Interface for Blender rendering."""

    def __init__(self, scene: BlenderScene):
        """Initialize the interface with a Blender scene."""
        self.scene = scene

    @classmethod
    def from_scene(cls, scene: BlenderScene):
        """Create a BlenderRenderer object from an existing scene."""
        return cls(scene)

    def render_snapshot(self, snapshot: Snapshot):
        """Render a snapshot of the scene."""
        # Set the resolution and output path
        self.scene.blender_scene.render.resolution_x = snapshot.xpix
        self.scene.blender_scene.render.resolution_y = snapshot.ypix
        self.scene.blender_scene.render.resolution_percentage = snapshot.percentage
        self.scene.blender_scene.render.filepath = snapshot.output_name
        # Take picture of current visible scene
        bpy.context.scene.cycles.samples = SCENE_SAMPLES
        bpy.ops.render.render(write_still=True)

    def create_bounding_boxes(
        self, camera: BlenderElement, elements: List[BlenderElement], file_path: str
    ):
        """Create bounding boxes for the elements in the scene."""
        raise NotImplementedError


def render_sweep_from_config(config: RenderingConfig):
    """Render a sweep from a configuration."""
    # Load Blender scene
    bpy.ops.wm.open_mainfile(filepath=config.scene_config.scene_path)

    # Initialize the scene, sweep, and renderer
    scene: BlenderScene = BlenderScene.from_scene_config(config.scene_config)
    sweep: BlenderSweep = BlenderSweep.from_sweep_config(config.sweep_config)
    renderer: BlenderRenderer = BlenderRenderer.from_scene(scene)

    for snapshot in tqdm(sweep.snapshots, desc="Rendering snapshots"):
        # Prepare axis, camera and light
        scene.prepare_from_snapshot(snapshot)

        # Render the snapshot, and create bounding boxes
        renderer.render_snapshot(snapshot, config.target_path)
        renderer.create_bounding_boxes(scene.camera, scene.elements, config.file_path)
