"""Package only the runtime files, with __init__.py at the archive root."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
destination = root / "dist" / "scholarrx-question-lookup-1.0.0.ankiaddon"
destination.parent.mkdir(exist_ok=True)
with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
    for name in ("__init__.py", "lookup.py", "manifest.json", "mapping.json"):
        archive.write(root / "scholarrx" / name, name)
with ZipFile(destination) as archive:
    assert archive.testzip() is None
print(destination)
