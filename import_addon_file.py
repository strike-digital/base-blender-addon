import ast
import shutil
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--destination")
args = parser.parse_args()


def main():
    destination = Path(args.destination) if args.destination else Path().cwd()
    if destination.suffix:
        destination = destination.parent

    print()

    # Get valid files
    from_folders = [Path(__file__).parent / "base_addon", Path(__file__).parent / "library"]
    all_files = []
    i = 0
    print(from_folders)
    for from_folder in from_folders:
        print(f"{from_folder.name}:")
        files = [file for file in from_folder.glob("**/*.py") if file.stem != "__init__"]
        all_files += files

        folder = from_folder
        for file in files:

            sub_folder = file.relative_to(from_folder).parents[0]
            if folder != sub_folder:
                folder = sub_folder

            print(f"  ({i}) {file.name}")
            i += 1

    print()
    idx = int(input("Enter the index of the file to create: "))
    file = all_files[idx]

    def get_file_imports(file: Path) -> set[Path]:
        """Recursively get a list of all relative inputs in a file"""
        with open(file, "r") as f:
            tree = ast.parse(f.read())

        imports_from = set()

        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                # Get only relative imports (the level is the number of dots in the import statement)
                if not node.level:
                    continue

                directory = file.parents[node.level - 1]
                parts = node.module.split('.')

                for subdir in parts[:-1]:
                    directory = directory / subdir

                node_file = directory / (parts[-1] + ".py")
                imports_from.add(node_file)
                imports_from = imports_from.union(get_file_imports(node_file))

        return imports_from

    files: list[Path] = [file] + list(get_file_imports(file))

    overwrite = True

    # Deal with existing files
    for file in files:
        if file.exists():
            print(f"Destination file '{file.name}' already exists:")
            print("(0) Overwrite")
            print("(1) Pass over")
            print("(2) Cancel")
            print()
            idx = int(input("Choose what to do with existing files: "))
            if idx == 2:
                print("Cancelled")
                return
            overwrite = idx != 1
            break

    # Copy files
    for file in files:
        dest = destination / file.name
        if file.exists() and not overwrite:
            print(f"Passed over existing file '{dest.name}'")
            continue
        shutil.copy(file, dest)
        print(f"Copied file '{file}' to '{dest}'")


if __name__ == "__main__":
    main()