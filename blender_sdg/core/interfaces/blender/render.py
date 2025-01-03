from blender_sdg.core.interfaces.blender.scene import BlenderScene
from blender_sdg.core.interfaces.blender.sweep import BlenderSweep
from blender_sdg.core.interfaces.blender.object import BlenderElement
from blender_sdg.config import RenderingConfig
from blender_sdg.core.interfaces.blender import utils

from blender_sdg.core.model import Dataset, Annotation, SnapshotAnnotation

import bpy
from tqdm import tqdm
from typing import List, Tuple
import uuid
import warnings
import numpy as np


class BlenderRenderer:
    """Interface for Blender rendering."""

    def __init__(
        self,
        scene: BlenderScene,
        target_path: str,
        resolution: Tuple[int, int],
        samples: int,
    ):
        """Initialize the interface with a Blender scene.

        Parameters:
        ___________
        scene: BlenderScene
            The Blender scene to render.
        target_path: str
            The path to save the rendered snapshots.
        resolution: Tuple[int, int]
            The resolution of the rendered snapshots.
        samples: int
            The number of samples to use for the rendered snapshots.
        """
        self.scene = scene
        self.target_path = target_path
        self.resolution = resolution
        # Set blender scene settings
        self.scene.blender_scene.render.resolution_x = resolution[0]
        self.scene.blender_scene.render.resolution_y = resolution[1]
        self.scene.blender_scene.cycles.samples = samples

    @classmethod
    def from_scene(
        cls,
        scene: BlenderScene,
        target_path: str,
        resolution: Tuple[int, int],
        samples: int,
    ):
        """Create a BlenderRenderer object from an existing scene."""
        return cls(scene, target_path, resolution, samples)

    def render_snapshot(
        self,
        snapshot_id: uuid.UUID,
    ) -> str:
        """Render a snapshot of the scene and return the path to the snapshot."""
        # Take picture of current visible scene and save it to the target path
        self.scene.blender_scene.render.filepath = (
            f"{self.target_path}/{snapshot_id}.png"
        )
        bpy.ops.render.render(write_still=True)

    def annotate_snapshot(
        self,
        cameras: List[BlenderElement],
        elements: List[BlenderElement],
        snapshot_id: uuid.UUID,
        relative: bool = True,
    ) -> Annotation:
        """Create bounding boxes for the elements in the scene."""
        if len(cameras) > 1:
            warnings.warn(
                "Multiple cameras are not supported yet. Only the first camera will be used."
            )
        camera = cameras[0]

        annotation = Annotation(
            file_name=f"{snapshot_id}.png",
            objects=SnapshotAnnotation(bbox=[], categories=[]),
        )

        for i, element in enumerate(elements):
            bounding_box: np.ndarray = utils.create_bounding_box(
                scene=self.scene,
                camera=camera,
                element=element,
                relative=relative,
                resolution=self.resolution,
            )
            if bounding_box is None:
                continue

            annotation.objects.bbox.append(bounding_box.tolist())
            annotation.objects.categories.append(i)

        return annotation


def generate_dataset_from_config(config: RenderingConfig) -> Dataset:
    """Generate a dataset from a rendering configuration."""
    # Initialize the scene and sweep
    scene: BlenderScene = BlenderScene.from_scene_config(config.scene_config)
    sweep: BlenderSweep = BlenderSweep.from_sweep_config(config.sweep_config)

    # Initialize the renderer
    renderer: BlenderRenderer = BlenderRenderer.from_scene(
        scene,
        config.target_path,
        config.resolution,
        config.samples,
    )

    # Initialize the dataset
    dataset: Dataset = Dataset(path=config.target_path, annotations=[])

    # Collect the dataset annotations
    for snapshot in tqdm(sweep.snapshots, desc="Rendering snapshots"):
        # Prepare axis, camera and light
        scene.prepare_from_snapshot(snapshot=snapshot)
        # Render the snapshot, and create bounding boxes
        renderer.render_snapshot(snapshot_id=snapshot.id)
        # Create bounding boxes
        annotation: Annotation = renderer.annotate_snapshot(
            cameras=scene.cameras,
            elements=scene.elements,
            snapshot_id=snapshot.id,
        )
        if config.debug:
            utils.draw_bounding_box_with_category(
                target_path=config.target_path,
                annotation=annotation,
                snapshot=snapshot,
            )

        dataset.annotations.append(annotation)

    return dataset
