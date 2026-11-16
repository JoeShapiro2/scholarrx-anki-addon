# ScholarRx Question Lookup

An Anki Desktop add-on that turns ScholarRx question IDs into a search for existing
AnKing notes. It opens Browse; users decide what to do with the resulting cards.
It does not import cards, change scheduling, unsuspend cards, or contact a website.

**Question IDs only map for ScholarRx's "Step 1 Qmax High-Yield Topics".**
Question IDs from other ScholarRx question banks or sections are not supported.

**The mappings are based on the "AnKing Step Deck" (11/15/2026).** Newer versions might not be supported.

## Install and use

1. In Anki Desktop, open **Tools → Add-ons → Install from file…**.
2. Select `dist/scholarrx-question-lookup-0.1.0.ankiaddon` and restart Anki.
3. Choose **Tools → Find cards from ScholarRx**.
4. Enter full question IDs, for example `1171.21, 1175.21,` and click OK.

Commas, spaces, tabs, newlines, and trailing commas are accepted. Duplicate IDs
and shared note matches are deduplicated. Decimal suffixes are preserved exactly.
Unknown IDs are reported; mapped IDs still open in Browse. If all IDs are unknown,
no browser search is launched. Weak matches are included as requested.

The corresponding notes must already be installed with a searchable field named
exactly `ankihub_id`. A quick compatibility check in Browse is:

```
ankihub_id:32869230-ea5b-4ea2-8510-a7bc407d1f70
```

If this returns nothing, confirm the note exists and its UUID is in the correct
field. A mapping can exist even if a student has none of its notes installed;
in that case Browse will show zero matches. This is distinct from an unknown QID.
One mapped note may generate multiple cloze cards.

## Mapping and limitations

The bundled lookup comes from the supplied `ScholarRx_QID_to_AnKing.xlsx`, sheet
`By QID`. It includes all 2,282 questions, including 66 labeled weak. These quality
labels come from the source workbook and are not independently validated.
Only identifiers and quality labels are bundled, not question text or card content.
The workbook is not changed. Future ScholarRx questions need a mapping update.

Designed for modern Anki Desktop (Qt6). It is not a mobile add-on. The lookup logic
is automatically tested; installation and dialog behavior still require a live
Anki smoke test. No affiliation with ScholarRx, AnKing, or AnkiHub is claimed.

## Development

The add-on uses Python's standard library and Anki's built-in APIs only.
To regenerate the mapping, use Python with `openpyxl` installed:

```
python tools/convert_mapping.py "D:\Documents\ScholarRx_QID_to_AnKing.xlsx" scholarrx/mapping.json
python -m unittest discover -s tests -v
python tools/build.py
```

Manual smoke test: cancel the dialog; try empty input; search `1171.21,`; search
`1171.21 1175.21`; search `1171.21, 99999999.99`; then try only the unknown ID.
Verify mixed input reports the unknown ID and still opens the valid results,
and that no notes or review schedules were changed.
