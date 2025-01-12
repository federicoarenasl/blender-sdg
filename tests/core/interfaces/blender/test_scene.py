import pytest
from blender_sdg.core.interfaces.blender.scene import BlenderScene
from blender_sdg.core.model import Snapshot
from blender_sdg.config.config import config_from_yaml, RenderingConfig
import yaml

from blender_sdg.core.model import Element

TEST_SCENE_PATH = "tests/core/interfaces/blender/basic-scene.blend"
CONFIG_PATH = "tests/config/test.config.yaml"


@pytest.fixture
def config() -> RenderingConfig:
    with open(CONFIG_PATH, "r") as file:
        yaml_config = yaml.safe_load(file)

    return config_from_yaml(yaml_config)


@pytest.fixture
def scene(config: RenderingConfig):
    return BlenderScene.from_scene_config(config.scene_config)


def test_scene_from_config(scene: BlenderScene):
    assert isinstance(scene, BlenderScene)
    assert scene.name == "Scene"
    assert len(scene.cameras) == 1
    assert len(scene.lights) == 1
    assert len(scene.axis) == 1
    assert len(scene.elements) == 2
    assert isinstance(scene.elements[0], Element)
    assert isinstance(scene.elements[1], Element)


def test_scene_init(scene: BlenderScene):
    test_scene = BlenderScene(
        blender_scene=scene.blender_scene,
        name=scene.name,
        cameras=scene.cameras,
        lights=scene.lights,
        axis=scene.axis,
        elements=scene.elements,
    )
    assert test_scene == scene


def test_prepare_from_snapshot(scene: BlenderScene):
    import mathutils
    import math

    snapshot = Snapshot(yaw=30, roll=45, camera_height=10, light_energy=5)
    scene.prepare_from_snapshot(snapshot)

    axis_location = scene.axis[0].object.location
    axis_rotation = scene.axis[0].object.rotation_euler
    camera_location = scene.cameras[0].object.location

    assert axis_location == mathutils.Vector((0.0, 0.0, 0.0))
    assert axis_rotation == mathutils.Euler(
        (math.radians(30.0), math.radians(45.0), 0.0)
    )
    assert camera_location == mathutils.Vector((0.0, 0.0, 10.0))
