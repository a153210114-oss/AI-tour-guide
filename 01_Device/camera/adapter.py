from __future__ import annotations

from pathlib import Path
from typing import Protocol

from importlib import import_module

VisionObservation = import_module("02_Scene_Context.models").VisionObservation


class CameraVisionAdapter(Protocol):
    """Boundary for local or hosted vision providers.

    Implementations return observations only. They do not select the final place;
    GPS, route, sequence and guide context remain the matching engine's job.
    """

    def observe(self, image_path: Path) -> VisionObservation:
        ...

