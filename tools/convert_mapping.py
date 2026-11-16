"""Convert the supplied By QID workbook into the add-on's bundled lookup.

Requires openpyxl for this development step only; Anki needs no extra packages.
"""

import argparse
import hashlib
import json
from pathlib import Path
from uuid import UUID

import openpyxl


def convert(source, destination):
    workbook = openpyxl.load_workbook(source, read_only=True, data_only=True)
    try:
        rows = workbook["By QID"].iter_rows(values_only=True)
        headers = next(rows)
        questions = {}
        for values in rows:
            row = dict(zip(headers, values))
            if row.get("QID") is None:
                continue
            qid = str(row["QID"]).strip()
            if qid in questions:
                raise ValueError("Duplicate question ID: " + qid)
            ids = list(dict.fromkeys(str(UUID(value.strip())) for value in
                       str(row.get("AnkiHub IDs") or "").splitlines() if value.strip()))
            if not ids:
                raise ValueError("No AnkiHub IDs for " + qid)
            questions[qid] = {"ankihub_ids": ids, "quality": row.get("Match Quality")}
        output = {"schema_version": 1, "source": source.name,
                  "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                  "questions": questions}
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"Converted {len(questions)} questions to {destination}")
    finally:
        workbook.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    convert(args.source, args.destination)
