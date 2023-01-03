from datetime import datetime
import argparse
from pathlib import Path
import warnings
import pandas as pd
from re import compile, sub

pattern = compile('\\W')

def ct(txt: str, repl:str = '.') -> str:
    """
    Transform input text to make it suitable for use as a IRI fragment

    :param txt: Input text
    :param repl: replacement character
    :return: Cleaned text
    """
    return sub(pattern, repl, txt)


def verify_args(args) -> None:
    """
    Ensure that no worksheets are included and excluded

    :param args: parsed arguments
    :return:
    """
    df = pd.read_excel(args.xlsx, sheet_name=None)
    if args.exclude is not None:
        for e in args.exclude:
            if args.include is not None:
                if e in args.include:
                    warnings.warn(f'Worksheet {e} is excluded and included')
            if e not in df:
                warnings.warn(f'Worksheet {e} is excluded but does not appear in the workbook')
    if args.include is not None:
        for i in args.include:
            if i not in df:
                warnings.warn(f'Worksheet {i} is included but does not appear in the workbook')


def cli() -> argparse.Namespace:
    """
    Create SHACL elements in an EDG ontology from Excel workbook metadata

options:
  -h, --help            show this help message and exit
  --input_ontology INPUT_ONTOLOGY
                        A turtle format ontology file exported from EDG
  --output_ontology OUTPUT_ONTOLOGY
                        A turtle format ontology file containing SHACL
                        elements plus the input ontology
  --xlsx XLSX           Excel workbook file from which metadata is harvested
  --exclude EXCLUDE     Name worksheet to exclude
  --include INCLUDE     Name of worksheet to include

By default all worksheets are included

    :return: Parsed arguments
    """
    print(ts(), 'Checking command parameters')
    ap = argparse.ArgumentParser(epilog='By default all worksheets are included',
                                 description='Create SHACL elements in an EDG ontology from Excel workbook metadata')
    ap.add_argument('--input_ontology', type=Path, required=True,
                    help='A turtle format ontology file exported from EDG')
    ap.add_argument('--output_ontology', type=Path, required=True,
                    help='A turtle format ontology file containing SHACL elements plus the input ontology')
    ap.add_argument('--xlsx', type=Path, required=True,
                    help='Excel workbook file from which meta data is harvested')
    ap.add_argument('--exclude', type=str, required=False, action='append',
                    help='Name worksheet to exclude')
    ap.add_argument('--include', type=str, required=False, action='append',
                    help='Name of worksheet to include')
    args = ap.parse_args()
    verify_args(args)
    return args


def ts() -> str:
    """
    Current time in ISO format

    :return: Current time in ISO format
    """
    return datetime.now().isoformat()
