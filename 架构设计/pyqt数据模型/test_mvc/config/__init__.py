import sys
import tomllib


with open("config/settings.toml", "rb") as f:
    settings = tomllib.load(f)

sys.path.append(settings['path_to_append']['Yplug'] + "/utils")
import cgtw_utils as cgt
from Y_utils import Yprint