import yaml
from blender_sdg.config.config import config_from_yaml, RenderingConfig
from blender_sdg.config.config import SweepConfig
import pytest


CONFIG_PATH = "tests/config/test.config.yaml"


@pytest.fixture
def config() -> RenderingConfig:
    with open(CONFIG_PATH, "r") as file:
        yaml_config = yaml.safe_load(file)

    return config_from_yaml(yaml_config)


def test_config_type(config: RenderingConfig):
    assert isinstance(config, RenderingConfig)


def test_config_from_yaml(config: RenderingConfig):
    assert config.engine == "blender"
    assert config.target_path == "dataset/train"
    assert config.debug is True
    assert config.random_seed == 0
    assert config.resolution == (256, 256)
    assert config.samples == 64


def test_scene_config(config: RenderingConfig):
    assert (
        config.scene_config.scene_path
        == "tests/core/interfaces/blender/basic-scene.blend"
    )
    assert config.scene_config.scene_name == "Scene"
    assert config.scene_config.camera_names == ["Camera"]
    assert config.scene_config.axis_names == ["Axis"]
    assert config.scene_config.element_names == ["obj_01", "obj_02"]
    assert config.scene_config.light_names == ["Light"]


def test_sweep_config_type(config: RenderingConfig):
    assert isinstance(config.sweep_config, SweepConfig)


def test_sweep_config(config: RenderingConfig):
    assert config.sweep_config.name == "example_sweep"
    assert config.sweep_config.step == 90
    assert config.sweep_config.yaw_limits == (-180.0, 180.0)
    assert config.sweep_config.roll_limits == (180.0, 180.0)
    assert config.sweep_config.camera_height_limits == (1.0, 1.0)
    assert config.sweep_config.light_energy_limits == (1000.0, 1000.0)
