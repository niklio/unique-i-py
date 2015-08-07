# -*- coding: utf-8 -*-
import re, pdb

class Document(object):

    def __init__(self, doc_id, features, width=2, reg=r'[\w\u4e00-\u9fcc]+'):
        """
        `width` designates the size of feature ngrams

        `reg` is used to tokenize the string
        """
        self.id = doc_id
        self.features = features

        self.width = width
        self.reg = reg

    def __repr__(self):
        return "<Document %s>" % (self.id)

    def _grams(self, feature):
        return list(map(list, zip(*[re.findall(self.reg, feature)[i:] + [''] * i  for i in range(self.width)])))

    def shingles(self):
        shingle_matrix = []
        
        for feature in self.features:
            if feature == None:
                shingle_matrix.append([])
                continue
            tokens = self._grams(feature)
            shingle_matrix.append(list(map(lambda x: Fingerprint(self.id, x), tokens)))

        return shingle_matrix


class Fingerprint(object):

    def __init__(self, doc_id, token):
        self.id = doc_id
        self.token = token

        self.value = hash(''.join(token))

    def __repr__(self):
        return "<Fingerprint: %s>" % (self.id)