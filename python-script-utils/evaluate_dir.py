import os
from pathlib import Path

root_dir = Path(os.getcwd()).parent.absolute()
def evaluate_dir(key, all_dirs):
    result = root_dir / all_dirs[key]
    assert (os.path.isdir(result), "Invalid directory evaluation, are you running this script from the correct directory?")
    return result