# -*- coding: utf-8 -*-
"""
(cre) module post-installation tests.
"""

import unittest

import cre


def simple_search(pattern, string):
    """
    Perform pattern search without compiling pattern.
    """
    return True if cre.search(pattern, string) else False


def compiled_pattern_search(pattern, string):
    """
    Perform compiled pattern search.
    """
    cp = cre.compile(pattern)
    return True if cp.search(string) else None


class CRETests(unittest.TestCase):
    """
    (cre) module basic tests.
    """

    pat_s = 'Кракозя.*'
    pat_s1 = '^акозя.*'
    pat_b = b'^.*unintelligible.*$'
    pat_u = u'.*characters'
    str_s = 'Кракозябры means unintelligible sequence of characters'
    str_b = b'krakozyabry means unintelligible sequence of characters'
    str_u = u'Кракозябры means unintelligible sequence of characters'

    def test_simple_search(self):
        """
        Test pattern search without compiling pattern.
        """
        self.assertTrue(simple_search(self.pat_s, self.str_s),
                        '{0} should match with {1}'
                        .format(self.pat_s, self.str_s))
        self.assertFalse(simple_search(self.pat_s1, self.str_s),
                         '{0} should not match with {1}'
                         .format(self.pat_s1, self.str_s))

    def test_compiled_pattern_search(self):
        """
        Test pattern search with compiled pattern.
        """
        self.assertTrue(compiled_pattern_search(self.pat_s, self.str_s),
                        '{0} should match with {1}'
                        .format(self.pat_s, self.str_s))
        self.assertFalse(compiled_pattern_search(self.pat_s1, self.str_s),
                         '{0} should not match with {1}'
                         .format(self.pat_s1, self.str_s))

    def test_string_params(self):
        """
        Test strings as parameters.
        """
        self.assertTrue(simple_search(self.pat_s, self.str_s),
                        '{0} should match with {1}'
                        .format(self.pat_s, self.str_s))

    def test_byte_params(self):
        """
        Test bytes as parameters.
        """
        self.assertTrue(simple_search(self.pat_b, self.str_b),
                        '{0} should match with {1}'
                        .format(self.pat_b, self.str_b))

    def test_unicode_params(self):
        """
        Test unicodes as parameters.
        """
        self.assertTrue(simple_search(self.pat_u, self.str_u),
                        u'{0} should match with {1}'
                        .format(self.pat_u, self.str_u))
