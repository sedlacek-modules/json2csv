#!/usr/bin/env python3
"""
json2csv

A command-line tool to convert JSON files to CSV format.

Usage:
    python3 json2csv.py [OPTIONS] [INPUT_FILES...]

Options:
    -h, --help           Show this help message and exit
    --line-delimited     Expect line-delimited JSON format on input

Author: Jaromir Sedlacek

Copyright (c) 2023 Jaromir Sedlacek

License: MIT
"""

import sys
import json
import csv
from io import IOBase
from typing import List, Dict, TextIO


def extract_keys(json_data: List[Dict]) -> List[str]:
    """
    Extracts unique keys from JSON data while preserving the order.

    :param json_data: List of JSON objects.
    :type json_data: List[Dict]
    :return: List of unique keys in the JSON data.
    :rtype: List[str]
    """
    keys = {}
    for row in json_data:
        keys.update(row)
    return list(keys.keys())


def load_json(open_file: TextIO, *, line_delimited: bool = False) -> List[Dict]:
    """
    Load JSON data from a file.

    :param open_file: The file object to read JSON data from.
    :type open_file: IOBase
    :param line_delimited: Flag indicating if the input is line-delimited JSON. Defaults to False.
    :type line_delimited: bool
    :return: List of dictionaries representing the loaded JSON data.
    :rtype: List[Dict]
    :raises ValueError: If the JSON format is invalid.
    """
    try:
        if line_delimited:
            result = []
            for line in open_file:
                data = json.loads(line)
                assert isinstance(data, dict), "Invalid line-delimited JSON format, expecting Dict\nDict\n..."
                result.append(data)
            return result
        else:
            result = json.load(open_file)
            assert isinstance(result, list), "Invalid json format, expecting List[Dict]"
            return result
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format") from e


def dump_csv(data: List[Dict], open_file: TextIO):
    """
    Dump data to a CSV file.

    :param data: List of dictionaries representing the data.
    :type data: List[Dict]
    :param open_file: The file object to write the CSV data to.
    :type open_file: IOBase
    :return: None
    """
    keys = extract_keys(data)
    writer = csv.DictWriter(open_file, fieldnames=keys, dialect='excel')
    writer.writeheader()
    writer.writerows(data)


def main(*file_names, line_delimited: bool = False, output_file: str = None):
    """
    Convert JSON files to CSV format.

    :param file_names: Input file names.
    :type file_names: Tuple[str]
    :param line_delimited: Flag indicating if the input is line-delimited JSON. Defaults to False.
    :type line_delimited: bool
    :param output_file: Output file name. If not provided, the result will be printed to stdout.
    :type output_file: str
    :return: None
    """
    # Load JSON files
    if file_names:
        records = []
        for name in file_names:
            with open(name, 'r') as r:
                records.extend(load_json(r, line_delimited=line_delimited))
    else:
        records = load_json(sys.stdin, line_delimited=line_delimited)

    # Dump CSV
    if output_file:
        with open(output_file, 'w') as w:
            dump_csv(records, w)
    else:
        dump_csv(records, sys.stdout)


if __name__ == '__main__':
    # Get command-line arguments excluding the script name
    args = sys.argv[1:]

    if "-h" in args or "--help" in args:
        print(__doc__.strip())
        sys.exit(0)

    line_delimited = '--line-delimited' in args
    if line_delimited:
        args.remove('--line-delimited')

    main(*args, line_delimited=line_delimited)
#