"""
Make your code unique

Example run:
env/bin/python main.py \
    --source tests/data/main.py \
    --target build/main.py
"""

import argparse
from pathlib import Path
import re


def _args():
    """ Request command line args """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='Full path to source code',
    )
    parser.add_argument(
        '--target',
        type=str,
        required=True,
        help='Full path to build',
    )

    return parser.parse_args()


def main(args: argparse.Namespace):
    source_path = args.source
    target_path = args.target

    target_data = ""
    source_lines = 1
    source_files = 1
    target_lines = 0
    target_files = 1

    source_dir = Path(source_path).parent
    # TODO: nested files
    source_libs = {
        file.name if file.is_dir() else file.name.split('.')[0]
        for file in source_dir.iterdir()
        if file.is_dir() or '.py' in file.name
    }

    with open(source_path, 'r') as file:
        source_data = file.read()
    source_lines += source_data.count("\n")

    is_comment = False
    for row in source_data.split("\n"):
        row_strip = row.strip()

        # Comments
        if row_strip == "\"\"\"":
            is_comment = not is_comment
        if is_comment or (row_strip and row_strip[0] == "#"):
            continue

        # Libs
        if 'from' in row and 'import' in row:
            lib_name = re.sub(r'^.*from +([a-z.]+) +import.*$', r'\1', row)

            # TODO: nested libs
            if lib_name in source_libs:
                lib_path = f"{source_dir}/{lib_name}/__init__.py" # FIXME

                with open(lib_path, 'r') as file:
                    source_data = file.read()
                source_files += 1
                source_lines += source_data.count("\n")

        target_data += row + "\n"

    target_lines += target_data.count("\n")

    # Delete last
    target_data = target_data[:-1]

    with open(target_path, 'w') as file:
        print(target_data, end="", file=file)

    print(
        f"Compressed {source_lines} lines in {source_files} files"
        f" → {target_lines} lines in {target_files} files"
    )


if __name__ == '__main__':
    main(_args())
