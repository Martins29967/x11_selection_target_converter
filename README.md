# x11_selection_target_converter

Translate between X11 selection target atom names (`UTF8_STRING`, `COMPOUND_TEXT`, `TEXT`, `STRING`) and their MIME type equivalents.

```python
from x11_selection_target_converter import atom_to_mime, mime_to_atom

atom_to_mime("UTF8_STRING")
# 'text/plain;charset=utf-8'

mime_to_atom("text/plain;charset=utf-8")
# 'UTF8_STRING'

atom_to_mime("APPLICATION_X_CUSTOM")
# 'APPLICATION_X_CUSTOM'
```

## Why this exists

X11 selections identify their payload with atoms such as `UTF8_STRING`, while most modern clipboard and drag-and-drop code speaks MIME. The two vocabularies overlap only partially, and there is no authoritative registry that maps one to the other. This library encodes the handful of mappings that are actually useful and leaves everything else alone.

The trade-off is deliberate: unknown atoms and MIME types are returned unchanged rather than raising. Selection targets are frequently application-specific, and a fallback-oriented pipeline (`try to convert, otherwise use as-is`) should not need exception handling for the common case.

## API

- `ATOM_TO_MIME` — dict mapping canonical atom names to MIME types.
- `MIME_TO_ATOM` — dict mapping canonical MIME types to atom names.
- `atom_to_mime(atom)` — translate an atom name to a MIME type. Unknown atoms are returned stripped of surrounding whitespace.
- `mime_to_atom(mime)` — translate a MIME type to an atom name. Unknown MIME types are returned stripped of surrounding whitespace.
- `normalize_atom(atom)` — strip and uppercase an atom name.
- `normalize_mime(mime)` — strip and lowercase a MIME type.

## Edge cases

Lookups are case-insensitive: `atom_to_mime("utf8_string")` and `mime_to_atom("TEXT/PLAIN")` both work. MIME parameters are compared as exact strings, so `text/plain; charset=utf-8` (with a space after the semicolon) is not recognized and is returned unchanged. If you need that form to match, normalize it before calling.
