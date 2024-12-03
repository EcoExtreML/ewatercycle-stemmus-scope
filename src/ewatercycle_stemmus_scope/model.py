"""eWaterCycle wrapper for the STEMMUS_SCOPE model."""
from collections.abc import ItemsView
from pathlib import Path
from typing import Any

from ewatercycle.base.model import ContainerizedModel, eWaterCycleModel
from ewatercycle.container import ContainerImage
from ewatercycle.base.parameter_set import ParameterSet

class StemmusScopeMethods(eWaterCycleModel):
    """The eWatercycle STEMMUS_SCOPE model.
    """
    forcing: None  # The model has no eWaterCycle forcing class.
    parameter_set: ParameterSet  # The model requires a parameter set (incl. forcing)

    _config: dict = {}

    def _make_cfg_file(self, **kwargs) -> Path:
        """Write model configuration file."""

        for kwarg in kwargs:  # Write any kwargs to the config.
            self._config[kwarg] = kwargs[kwarg]

        config_file = self._cfg_dir / "config.txt"

        with config_file.open(mode="w") as f:
            f.write("")

        return config_file

    @property
    def parameters(self) -> ItemsView[str, Any]:
        return self._config.items()


class StemmusScope(ContainerizedModel, StemmusScopeMethods):
    """The STEMMUS_SCOPE eWaterCycle model, with the Container Registry docker image."""
    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/ecoextreml/stemmus_scope-grpc4bmi:1.6.1"
    )
