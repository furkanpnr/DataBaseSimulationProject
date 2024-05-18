import os
from pathlib import Path

_path_joiner = lambda base_path, *paths: os.path.join(base_path, *paths)
