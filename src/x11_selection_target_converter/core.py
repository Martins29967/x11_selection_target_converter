"""Core conversion tables and helpers.

The X11 selection protocol names targets with atoms such as ``UTF8_STRING`` and
``COMPOUND_TEXT``. Clipboard and drag-and-drop layers usually speak MIME types
instead. There is no universal registry that maps one to the other, so this
module encodes the mappings that are useful in practice and leaves anything else
alone.

Case handling is deliberate: atom names are compared case-insensitively because
X11 atoms are interned by name and callers sometimes pass ``utf8_string`` from
configuration. MIME types are lowercased for the same reason. The returned
values use the canonical spelling from the tables below.
"""

from __future__ import annotations

# Canonical atom name -> canonical MIME type.
#
# TEXT is mapped to text/plain rather than text/plain;charset=utf-8 because the
# ICCCM TEXT target does not promise UTF-8; it is a legacy target whose encoding
# is locale-dependent. Callers that know the encoding should convert explicitly.
ATOM_TO_MIME = {
    "UTF8_STRING": "text/plain;charset=utf-8",
    "COMPOUND_TEXT": "text/plain;charset=compound-text",
    "TEXT": "text/plain",
    "STRING": "text/plain;charset=iso-8859-1",
}

# Canonical MIME type -> canonical atom name.
#
# The reverse map is not simply the inverse of ATOM_TO_MIME because several
# MIME types collapse onto the same atom. We choose the most specific atom that
# is still correct. For example text/plain;charset=utf-8 maps to UTF8_STRING,
# while bare text/plain maps to TEXT.
MIME_TO_ATOM = {
    "text/plain;charset=utf-8": "UTF8_STRING",
    "text/plain;charset=compound-text": "COMPOUND_TEXT",
    "text/plain": "TEXT",
    "text/plain;charset=iso-8859-1": "STRING",
}


def normalize_atom(atom: str) -> str:
    """Return the canonical spelling of an X11 target atom name.

    Atom names are ASCII in practice but we do not reject non-ASCII input;
    unknown names are returned stripped and uppercased, matching the convention
    used by X11 atom names. This keeps the function total and predictable.
    """
    return atom.strip().upper()


def normalize_mime(mime: str) -> str:
    """Return a normalized MIME type for table lookup.

    MIME types are case-insensitive per RFC 2045. We lowercase the whole string
    rather than parsing parameters, because the tables only contain a few exact
    strings and parsing would add failure modes without improving the result.
    """
    return mime.strip().lower()


def atom_to_mime(atom: str) -> str:
    """Translate an X11 selection target atom name to a MIME type.

    Unknown atoms are returned unchanged (after stripping surrounding
    whitespace) so that callers can pass them through to a fallback path. We do
    not raise, because selection targets are frequently application-specific and
    a raise would make the common "try to convert, otherwise use as-is" pattern
    awkward.
    """
    key = normalize_atom(atom)
    return ATOM_TO_MIME.get(key, atom.strip())


def mime_to_atom(mime: str) -> str:
    """Translate a MIME type to an X11 selection target atom name.

    Unknown MIME types are returned unchanged (after stripping surrounding
    whitespace). As with :func:`atom_to_mime`, this makes the function usable in
    a fallback-oriented pipeline without exception handling.
    """
    key = normalize_mime(mime)
    return MIME_TO_ATOM.get(key, mime.strip())
