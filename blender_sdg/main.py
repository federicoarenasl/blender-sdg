from blender_sdg.config import RenderingConfig
import blender_sdg.core.interfaces.blender.render as blender_renderer


def trigger_rendering_sweep(config: RenderingConfig):
    """Load a scene from a YAML configuration."""
    # Load the scene and sweep from the configuration
    if config.engine != "blender":
        raise ValueError(f"Unsupported engine: {config.engine}")
    else:
        blender_renderer.render_sweep_from_config(config)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Render a sweep of snapshots.")
    parser.add_argument(
        "--config_path", type=str, help="Path to the YAML configuration file."
    )
    args = parser.parse_args()

    # Load the configuration and render the sweep
    config = RenderingConfig(**json.load(open(args.config_path)))

    # Render the sweep
    trigger_rendering_sweep(config)
