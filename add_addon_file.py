
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

    # library_dir = Path(__file__).parent / "library"
    library_dir = Path(__file__).parent
    lib_files = {f.name: f for f in library_dir.rglob("**/*.py") if f.is_file()}

    if file.name in lib_files:
        if input(f"File {file.name} already exists in library at {lib_files[file.name].relative_to(library_dir)}, update? (y/n)\n") != "y":
            print("Exiting")
            return
        
        destination = lib_files[file.name]
    else:
        destination = library_dir / file.name

    if destination.exists():
        os.remove(destination)

    copyfile(file, destination)
    print(f"Copied file from \n{file}\nto\n{destination} successfully")


if __name__ == "__main__":
    main()
