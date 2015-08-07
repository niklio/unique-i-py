# -*- coding: utf-8 -*-
"""
test_dedupe
----------------------------------

Tests for `dedupe` module.
"""

import unittest

from dedupe import Dedupe, Document, Fingerprint

class TestDedupe(unittest.TestCase):

    def test_features(self):
        ids = ['1', '2', '3', '4', '5']
        featureset = [
            ['123', 'abc', 'xyz'],
            ['121', 'def', 'xyz'],
            ['321', 'cba', 'zyx'],
            ['999', 'mmm', 'jjj'],
            ['123', 'abc', 'xyz'],
        ]

        self.assertTrue(len(Dedupe(ids, featureset)._features()) == 3)
        self.assertTrue(all([len(feature) == 5 for feature in Dedupe(ids, featureset)._features()]))

    def test_groups(self):
        ids = [1, 2, 3]
        featureset = [
            ['cat', 'dog'],
            ['cat', 'dog'],
            ['dog', 'cat'],
        ]

        self.assertTrue(len(Dedupe(ids, featureset)._groups()) == 2)
        self.assertTrue(len(Dedupe(ids, featureset)._groups()[0]) == 1)


    def test_similarity(self):
        ids = [1, 2, 3]
        featureset = [
            ['a b c'],
            ['a b c'],
            ['a b d'],
        ]

        self.assertTrue(Dedupe(ids, featureset).similarity()[(1, 2)] == 2)
        self.assertTrue(Dedupe(ids, featureset).similarity()[(2, 3)] == 1)
        self.assertTrue(Dedupe(ids, featureset).similarity()[(1, 3)] == 1)

        self.assertFalse(Dedupe(ids, featureset).similarity()[(2, 1)])


class TestDocument(unittest.TestCase):

    def test_tokenize(self):

        def tokenizer(string, reg):
            return Document(1, '', 2, reg)._tokenize(string)

        self.assertTrue(tokenizer('', r'.') == '')
        self.assertTrue(tokenizer('the', r'.') == ['t', 'h', 'e'])
        self.assertTrue(tokenizer('the quick fox', r'\w+') == ['the', 'quick', 'fox'])

        self.assertFalse(tokenizer('a1a', r'[a-z]') == ['a', '1', 'a'])
        self.assertFalse(tokenizer('The #$#@ fox', r'[A-Za-z]+') == ['The', '#$#@', 'fox'])


    def test_grams(self):

        def ngrams(string, reg, width):
            return Document(1, '', width, reg)._grams(string)

        self.assertTrue(ngrams('', r'.', 1) == [['']])
        self.assertTrue(ngrams('', r'.', 3) == [['', '', '']])

        self.assertTrue(ngrams('a', r'.', 3) == [['a', '', '']])
        self.assertTrue(ngrams('a b', r'[a-z]', 3) == [['a', 'b', ''], ['b', '', '']])

        self.assertTrue(ngrams('a', r'.', 1) == [['a']])
        self.assertTrue(ngrams('The quick fox jumped', r'[A-Za-z]+', 3) == [['The', 'quick', 'fox'], ['quick', 'fox', 'jumped']])


    def test_shingles(self):

        def shingles(string):
            return Document(1, string, 2, r'\w+').shingles()

        self.assertTrue(shingles('') == [])

        self.assertFalse(shingles('a b') == shingles('a b'))
        self.assertFalse(shingles('a b') == shingles('b a'))




class TestFingerprint(unittest.TestCase):

    def test_fingerprint(self):
        token = "This is a document token"
        self.assertTrue(Fingerprint(1, token).value != Fingerprint(1, token).token == token)

        self.assertTrue(Fingerprint(123, "Same token => same hash").value == Fingerprint(123, "Same token => same hash").value)
        self.assertTrue(Fingerprint(321, "Different ids don't affect value").value == Fingerprint(123, "Different ids don't affect value").value)
        self.assertTrue(Fingerprint(123, ("Hashable", "data", "types", "are", "allowed")).value == Fingerprint(123, ("Hashable", "data", "types", "are", "allowed")).value)

        self.assertFalse(Fingerprint(123, "Different token").value == Fingerprint(123, "Different hash").value)
        self.assertFalse(Fingerprint(123, "1").value == Fingerprint(321, 1).value)


if __name__ == '__main__':
    unittest.main()


