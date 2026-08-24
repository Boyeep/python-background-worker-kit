from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PipelineDefinition:
    id: str
    name: str
    summary: str
    tags: list[str]
    runtime: str
    sample_outputs: list[str]
    handler: Callable[[np.ndarray], tuple[list[dict], list[dict], list[dict]]]
