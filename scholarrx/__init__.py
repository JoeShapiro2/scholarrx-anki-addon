"""ScholarRx question lookup for Anki Desktop."""

from functools import lru_cache
from pathlib import Path

from aqt import dialogs, mw
from aqt.qt import QAction
from aqt.utils import getText, showWarning

from .lookup import load_mapping, lookup, parse_qids


@lru_cache(maxsize=1)
def mapping():
    return load_mapping(Path(__file__).with_name("mapping.json"))


def show_dialog():
    if mw.col is None:
        showWarning("Open an Anki profile before looking up questions.")
        return
    raw, ok = getText(
        prompt="Paste ScholarRx question IDs (for example, 1171.21, 1175.21).\n"
        "Separate IDs with commas, spaces, or newlines.",
        title="Find cards from ScholarRx",
        parent=mw,
    )
    if not ok:
        return
    try:
        qids = parse_qids(raw)
        query, missing = lookup(qids, mapping())
    except (ValueError, OSError) as error:
        showWarning(str(error), parent=mw)
        return
    if missing:
        message = "No mapping found for: " + ", ".join(missing)
        if query:
            message += "\n\nContinuing with the other question IDs that have mappings. Click OK to view their cards."
        showWarning(message, parent=mw)
    if query:
        dialogs.open("Browser", mw, search=(query,))


action = QAction("Find cards from ScholarRx", mw)
action.triggered.connect(show_dialog)
mw.form.menuTools.addAction(action)
