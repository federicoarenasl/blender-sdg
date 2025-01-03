from blender_sdg.config import RenderingConfig, SupportedEngines, config_from_yaml
from blender_sdg.core.model import Dataset

import os


def generate_dataset(config: RenderingConfig):
    """Load a scene from a YAML configuration and trigger the rendering sweep."""
    # Check if the engine is supported
    if config.engine != SupportedEngines.BLENDER:
        raise ValueError(f"Unsupported engine: {config.engine}")

    # Check if the target path exists
    if os.path.exists(config.target_path):
        raise ValueError(
            f"The target path {config.target_path} already exists. Skipping dataset generation."
        )

    # Import the renderer and generate the dataset
    import blender_sdg.core.interfaces.blender.render as renderer

    dataset: Dataset = renderer.generate_dataset_from_config(config)

    # Save the dataset to the target path as a JSONL file
    with open(f"{config.target_path}/dataset.jsonl", "w") as f:
        for annotation in dataset.annotations:
            f.write(annotation.model_dump_json() + "\n")


if __name__ == "__main__":
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Render a sweep of snapshots.")
    parser.add_argument(
        "--config_path", type=str, help="Path to the YAML configuration file."
    )
    args = parser.parse_args()

    # Load the configuration and render the sweep
    with open(args.config_path, "r") as config_file:
        config = config_from_yaml(yaml.load(config_file, Loader=yaml.FullLoader))

    # Render the sweep
    generate_dataset(config)
