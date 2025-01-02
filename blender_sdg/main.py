from blender_sdg.config import RenderingConfig, SupportedEngines, config_from_yaml


def trigger_rendering_sweep(config: RenderingConfig):
    """Load a scene from a YAML configuration."""
    # Load the scene and sweep from the configuration
    if config.engine != SupportedEngines.BLENDER:
        raise ValueError(f"Unsupported engine: {config.engine}")

    import blender_sdg.core.interfaces.blender.render as blender_renderer

    blender_renderer.render_sweep_from_config(config)


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
    trigger_rendering_sweep(config)
