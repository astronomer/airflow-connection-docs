"""
This script copies the contents of the `dev` directory to the `target` directory. It does so by:
- accepting a target directory as an argument
- renaming the stage directory to stage_old
- copying the contents of the dev directory to the stage directory
- deleting the stage_old directory

Usage:
- python scripts/promote.py stage
- python scripts/promote.py prod
"""

import os, sys

from shutil import copytree, rmtree

# get the target directory from the command line
target = sys.argv[1]

dev_dir = os.path.join(os.path.dirname(__file__), "..", "connections", "dev")
target_dir = os.path.join(os.path.dirname(__file__), "..", "connections", target)

target_dir_old = target_dir + "_old"

# Clean up the stage_old directory if it exists
try:
    rmtree(target_dir_old)
except FileNotFoundError:
    print(f"{target}_old directory not found. No need to delete.")
    pass

# Rename the stage directory to stage_old
try:
    os.rename(target_dir, target_dir_old)
except FileNotFoundError:
    print(f"{target} directory not found. Creating new stage directory.")
    pass

# Copy the contents of the dev directory to the stage directory
copytree(dev_dir, target_dir)

# Delete the stage_old directory
try:
    rmtree(target_dir_old)
except FileNotFoundError:
    print(f"{target}_old directory not found. No need to delete.")
    pass

print(f"{target} directory updated.")
