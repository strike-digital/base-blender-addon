
import argparse
import os

from pathlib import Path
from shutil import copyfile


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file")
args = parser.parse_args()


def main():
    file = Path(args.file)
    if not file.exists():
        print("File does not exist!!")
        return

    library_dir = Path(__file__).parent / "library"
    lib_files = [f for f in library_dir.iterdir() if f.is_file() and f.suffix == ".py"]

    if file.name in [f.name for f in lib_files]:
        if input(f"File {file.name} already exists in library, update? (y/n)") != "y":
            print("Exiting")
            return
    
    destination = library_dir / file.name

    if destination.exists():
        os.remove(destination)

    copyfile(file, destination)
    print(f"Copied file from \n{file}\nto\n{destination} successfully")


if __name__ == "__main__":
    main()
