"""Public API for x11_selection_target_converter.

This package translates between X11 selection target atom names and MIME types.
The mapping is intentionally small and explicit: X11 has a handful of well-known
targets, and pretending the conversion is a general-purpose MIME database would
produce surprising results. Unknown targets are returned unchanged so callers can
decide how to handle them.
"""

from .core import (
    ATOM_TO_MIME,
    MIME_TO_ATOM,
    atom_to_mime,
    mime_to_atom,
    normalize_atom,
    normalize_mime,
)

__all__ = [
    "ATOM_TO_MIME",
    "MIME_TO_ATOM",
    "atom_to_mime",
    "mime_to_atom",
    "normalize_atom",
    "normalize_mime",
]
