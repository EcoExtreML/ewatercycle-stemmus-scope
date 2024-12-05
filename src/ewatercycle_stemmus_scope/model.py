"""eWaterCycle wrapper for the STEMMUS_SCOPE model."""
from pathlib import Path
from typing import Any

from ewatercycle.base.model import ContainerizedModel, eWaterCycleModel
from ewatercycle.container import ContainerImage
from ewatercycle.base.parameter_set import ParameterSet


def read_config(config_file: str | Path) -> dict[str, str]:
    config = {}
    with Path(config_file).open(encoding="utf8") as f:
        for line in f:
            (key, val) = line.split("=")
            config[key] = val.rstrip("\n")
    return config


def write_config(fname: Path, config: dict[str, Any]) -> None:
    with fname.open(mode="w", encoding="utf8") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")


class StemmusScopeMethods(eWaterCycleModel):
    """The eWatercycle STEMMUS_SCOPE model."""
    forcing: None  # The model has no eWaterCycle forcing class.
    parameter_set: ParameterSet  # The model requires a parameter set (incl. forcing)

    def _make_cfg_file(self, **kwargs) -> Path:
        """Write model configuration file."""
        config = read_config(self.parameter_set.directory / self.parameter_set.config)

        for kwarg in kwargs:  # Write any kwargs to the config.
            config[kwarg] = kwargs[kwarg]

        input_path = Path(config["InputPath"])
        if input_path.is_absolute() and not input_path.is_relative_to(self.parameter_set.config):
            msg = "Invalid parameterset: `InputPath` data is not relative to the config file!"
            raise ValueError(msg)
        if not input_path.is_absolute():
            input_path = self.parameter_set.directory / input_path
        if not input_path.exists():
            msg = f"No directory founds at {input_path}"
            raise ValueError(msg)
        config["InputPath"] = str(input_path) + "/"  # directories need to end in / for matlab code.

        # Prep working directory, output path
        for _dir in ("WorkDir", "OutputPath"):
            _path = self._cfg_dir / _dir
            _path.mkdir()
            config[_dir] = str(_path) + "/"

        output_cfg_file = self._cfg_dir / "STEMMUS_SCOPE_config.txt"
        write_config(output_cfg_file, config)

        return output_cfg_file


class StemmusScope(ContainerizedModel, StemmusScopeMethods):
    """The STEMMUS_SCOPE eWaterCycle model, with the Container Registry docker image."""
    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/ecoextreml/stemmus_scope-grpc4bmi:1.6.1"
    )
