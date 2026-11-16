"""Check every generated query against the source workbook's Anki Search column."""

import json
import sys
from pathlib import Path

import openpyxl

root = Path(__file__).resolve().parents[1]
mapping = json.loads((root / "scholarrx" / "mapping.json").read_text(encoding="utf-8"))["questions"]
workbook = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
checked = 0
links = 0
try:
    for row in workbook["By QID"].iter_rows(min_row=2, values_only=True):
        if row[1] is None:
            continue
        ids = mapping[str(row[1])]["ankihub_ids"]
        query = "(" + " OR ".join("ankihub_id:" + value for value in ids) + ")"
        assert query == row[8], f"Query mismatch for {row[1]}"
        checked += 1
        links += len(ids)
    assert checked == len(mapping)
finally:
    workbook.close()
print(f"Verified {checked} exact workbook queries and {links} question-note links.")
