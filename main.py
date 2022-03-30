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


def process_file(source_path):
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
    is_skipped = False
    for row in source_data.split("\n"):
        row_strip = row.strip()

        # Comments
        if row_strip == "\"\"\"":
            is_comment = not is_comment
            if not is_comment:
                continue
        if (
            is_comment
            or (row_strip and row_strip[0] == "#")
            or (len(row_strip) >= 3 and row_strip[:3] == "\"\"\"")
        ):
            continue

        # Lib data
        if "__version__" in row:
            continue
        if "__all__" in row:
            if not any(i in row for i in {")", "}"}):
                is_skipped = True
            continue
        if is_skipped:
            if any(i in row for i in {")", "}"}):
                is_skipped = False
            continue

        # Libs
        if "from" in row and "import" in row:
            lib_name = re.sub(r'^.*from +([a-z.]+) +import.*$', r'\1', row)

            # TODO: nested libs
            if lib_name in source_libs:
                lib_path = f"{source_dir}/{lib_name}/__init__.py" # FIXME
                lib_data, lib_lines, lib_files, res_lines, res_files = \
                    process_file(lib_path)

                target_data += lib_data
                source_lines += lib_lines
                source_files += lib_files

                continue

        #
        target_data += row + "\n"

    target_lines += target_data.count("\n")

    # Delete last
    target_data = target_data.strip()

    return target_data, source_lines, source_files, target_lines, target_files

def main(args: argparse.Namespace):
    source_path = args.source
    target_path = args.target

    target_data, source_lines, source_files, target_lines, target_files = \
        process_file(source_path)

    with open(target_path, 'w') as file:
        print(target_data, file=file)

    print(
        f"Compressed {source_lines} lines in {source_files} files"
        f" → {target_lines} lines in {target_files} files"
    )


if __name__ == '__main__':
    main(_args())
