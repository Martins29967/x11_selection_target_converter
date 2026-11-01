import unittest

from x11_selection_target_converter import (
    ATOM_TO_MIME,
    MIME_TO_ATOM,
    atom_to_mime,
    mime_to_atom,
    normalize_atom,
    normalize_mime,
)


class TestNormalizeAtom(unittest.TestCase):
    def test_uppercases_and_strips(self):
        self.assertEqual(normalize_atom("  utf8_string  "), "UTF8_STRING")

    def test_preserves_unknown_names_after_normalization(self):
        self.assertEqual(normalize_atom(" my_custom_atom "), "MY_CUSTOM_ATOM")


class TestNormalizeMime(unittest.TestCase):
    def test_lowercases_and_strips(self):
        self.assertEqual(normalize_mime("  Text/Plain;Charset=UTF-8 "), "text/plain;charset=utf-8")

    def test_preserves_parameters(self):
        self.assertEqual(normalize_mime("text/plain; charset=iso-8859-1"), "text/plain; charset=iso-8859-1")


class TestAtomToMime(unittest.TestCase):
    def test_known_atoms(self):
        self.assertEqual(atom_to_mime("UTF8_STRING"), "text/plain;charset=utf-8")
        self.assertEqual(atom_to_mime("COMPOUND_TEXT"), "text/plain;charset=compound-text")
        self.assertEqual(atom_to_mime("TEXT"), "text/plain")
        self.assertEqual(atom_to_mime("STRING"), "text/plain;charset=iso-8859-1")

    def test_case_insensitive_lookup(self):
        self.assertEqual(atom_to_mime("utf8_string"), "text/plain;charset=utf-8")
        self.assertEqual(atom_to_mime("  Compound_Text  "), "text/plain;charset=compound-text")

    def test_unknown_atom_returned_stripped(self):
        self.assertEqual(atom_to_mime("  APPLICATION_X_CUSTOM  "), "APPLICATION_X_CUSTOM")

    def test_empty_string(self):
        self.assertEqual(atom_to_mime(""), "")


class TestMimeToAtom(unittest.TestCase):
    def test_known_mime_types(self):
        self.assertEqual(mime_to_atom("text/plain;charset=utf-8"), "UTF8_STRING")
        self.assertEqual(mime_to_atom("text/plain;charset=compound-text"), "COMPOUND_TEXT")
        self.assertEqual(mime_to_atom("text/plain"), "TEXT")
        self.assertEqual(mime_to_atom("text/plain;charset=iso-8859-1"), "STRING")

    def test_case_insensitive_lookup(self):
        self.assertEqual(mime_to_atom("TEXT/PLAIN;CHARSET=UTF-8"), "UTF8_STRING")
        self.assertEqual(mime_to_atom("  Text/Plain  "), "TEXT")

    def test_unknown_mime_returned_stripped(self):
        self.assertEqual(mime_to_atom("  application/x-custom  "), "application/x-custom")

    def test_empty_string(self):
        self.assertEqual(mime_to_atom(""), "")

    def test_parameter_spacing_is_not_normalized(self):
        # The table contains exact strings, so an extra space before a parameter
        # is not a known MIME type and must be returned unchanged.
        self.assertEqual(
            mime_to_atom("text/plain; charset=utf-8"),
            "text/plain; charset=utf-8",
        )


class TestTables(unittest.TestCase):
    def test_tables_are_consistent(self):
        for atom, mime in ATOM_TO_MIME.items():
            self.assertEqual(MIME_TO_ATOM[mime], atom)

    def test_tables_are_not_mutated_by_calls(self):
        before_atom = dict(ATOM_TO_MIME)
        before_mime = dict(MIME_TO_ATOM)
        atom_to_mime("UTF8_STRING")
        mime_to_atom("text/plain")
        self.assertEqual(ATOM_TO_MIME, before_atom)
        self.assertEqual(MIME_TO_ATOM, before_mime)


if __name__ == "__main__":
    unittest.main()
