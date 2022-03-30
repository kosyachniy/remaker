"""
Make your code unique

Example run:
env/bin/python main.py \
    --source tests/data/main.py \
    --target build/main.py
"""

import argparse
from pathlib import Path


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

    source_lines = 0
    source_files = 1
    target_lines = 0
    target_files = 1

    source_dir = Path(source_path).parent
    target_data = ""

    with open(source_path, 'r') as file:
        source_data = file.read()

    is_comment = False
    for row in source_data.split("\n"):
        source_lines += 1

        if row == "\"\"\"":
            is_comment = not is_comment

        if is_comment:
            continue

        target_data += row + "\n"
        target_lines += 1

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
