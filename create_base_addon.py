import shutil
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--destination")

args = parser.parse_args()

destination = Path(args.destination) if args.destination else Path().cwd()
destination /= "new_addon"
from_folder = Path(__file__).parent / "base_addon"

shutil.copytree(from_folder, destination)