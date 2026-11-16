"""Pure lookup logic: no Anki imports and no collection modifications."""

import json
import re
from uuid import UUID


def parse_qids(raw):
    # Identifiers are strings: never discard suffixes or leading zeroes.
    qids = list(dict.fromkeys(part for part in re.split(r"[,\s]+", raw.strip()) if part))
    if not qids:
        raise ValueError("Enter at least one ScholarRx question ID.")
    invalid = [qid for qid in qids if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", qid)]
    if invalid:
        raise ValueError("Invalid question ID(s): " + ", ".join(invalid))
    return qids


def load_mapping(path):
    with open(path, encoding="utf-8") as source:
        data = json.load(source)
    if data.get("schema_version") != 1 or not isinstance(data.get("questions"), dict):
        raise ValueError("Unsupported ScholarRx mapping file. Reinstall the add-on.")
    questions = data["questions"]
    for qid, entry in questions.items():
        if not isinstance(entry, dict) or not isinstance(entry.get("ankihub_ids"), list):
            raise ValueError("Invalid mapping entry for " + qid)
        for identifier in entry["ankihub_ids"]:
            if not isinstance(identifier, str) or str(UUID(identifier)) != identifier:
                raise ValueError("Invalid AnkiHub ID for " + qid)
    return questions


def lookup(qids, questions):
    identifiers = []
    missing = []
    for qid in qids:
        entry = questions.get(qid)
        if not entry or not entry["ankihub_ids"]:
            missing.append(qid)
        else:
            identifiers.extend(entry["ankihub_ids"])
    terms = ["ankihub_id:" + identifier for identifier in dict.fromkeys(identifiers)]
    return ("(" + " OR ".join(terms) + ")" if terms else ""), missing
