# -*- coding: utf-8 -*-
import re, pdb

class Document(object):

    def __init__(self, *features, width=2, reg=r'[\w\u4e00-\u9fcc]+'):
        """
        `width` designates the size of feature ngrams

        `reg` is used to tokenize the string
        """

        self.id = id(self)
        self.features = features

        self.width = width
        self.reg = reg

    def __repr__(self):
        return "<Document %s>" % (self.id)

    def _grams(self, tokens):
        return set(zip(*[tokens[i:] for i in range(self.width)]))

    def _sketch(self):
        tokens_list = [re.findall(self.reg, feature.lower()) for feature in self.features]
        sketch = [self._grams(tokens) for tokens in tokens_list]
        return sketch

    def shingles(self):
        shingles_list = []
        sketch = self._sketch()

        for tokens in sketch:
            shingles = set()
            while tokens:
                shingles.add(Fingerprint(self.id, tokens.pop()))
                
            shingles_list.append(shingles)

        return shingles_list


class Fingerprint(object):

    def __init__(self, doc_id, token):
        self.id = doc_id
        self.token = token

        self.value = hash(''.join(token))

    def __repr__(self):
        return "<Fingerprint: %s>" % (self.id)