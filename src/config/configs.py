from pathlib import Path

import yaml
from addict import Dict

RESOURCES = Path("resources")

with open(RESOURCES / "config.yaml", encoding="utf-8") as f:
    config = Dict(yaml.load(f, Loader=yaml.SafeLoader))
