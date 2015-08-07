# -*- coding: utf-8 -*-
import re, itertools, collections

class Dedupe(object):


    def __init__(self, ids, featureset, threshhold, feature_weights=None):
        """
        `ids` is an N sized vector of unique ids for featureset

        `featureset` is a size N list of M features.

        `threshhold` is float between 0 and 1.
            threshhold of 1 => document A must be a subset of document B for A, B to be considered a duplicate pair.
            threshhold of 0 => document A's shingles and document B's shingles must be disjoint sets

        `feature_weights` is a M sized vector of weights
        """
        assert len(ids) == len(featureset)
        assert all([len(features) for features in featureset])

        self.ids = ids
        self.featureset = featureset
        self.features, self.number_of_features = _features(featureset)

        if threshhold <= 1 and threshhold >=0:
            self.threshhold = threshhold

        if feature_weights == None:
            self.feature_weights = [1] * self.number_of_features
        elif all([weight > 0 for weight in feature_weights]) and len(feature_weights) == self.number_of_features:
            self.feature_weights = feature_weights



    # Converts an MxN featureset into M features of fingerprints of n.
    def _features(self, featureset):
        assert len(row) > 1

        # Construct dictionary of documents for easy lookup.
        documents = {}
        for row in featureset:
            doc_id = row[0]
            documents[doc_id] = Document(doc_id, row[:1])

        # [[[]]] of fingerprints.  Documents > features > fingerprints
        fingerprints = [document.shingles() for document in documents.values()]

        # Every feature must be same size
        number_of_features = len(fingerprints[0])

        # Reorganize fingerprints by feature
        features = [[] for i in range(number_of_features)]
        for document in fingerprints:
            for i, feature in enumerate(document):
                for fingerprint in feature:
                    features[i].append(fingerprint)

        return features, number_of_features



    # Group fingerprints by hash value.
    def _groups(self, features):
        groups = [[] for i in range(len(features))]
        for i, feature in enumerate(features):
            for key, group in itertools.groupby(feature, lambda x: x.value):
                group = list(group)
                if len(group) > 1:
                    groups[i].append(group)

        return groups



    # Converts groups into a similarity dictionary.
    def _similarity(self, group):
        # Count similar fingerprints between document pairs
        similarity = collections.defaultdict(lambda:0)
        for i, feature in enumerate(grouped):
            for group in feature:
                ids = [fingerprint.id for fingerprint in group]
                if len(set(ids)) == 1:
                    continue
                pairs = list(itertools.combinations(ids, 2))
                for pair in pairs:
                    # Weight them
                    similarity[tuple(sorted(pair))] += self.feature_weights[i]

        return similarity



    def _jaccard(self, similarity):
        # Weighted jaccard coefficient must exceed threshold for a similar pair to be considered duplicates
        duplicates = []
        for id_pair, similarity in similarity.items():
            pair = [documents[doc_id] for doc_id in id_pair]
            pair_lengths = [0, 0]
            for i, document in enumerate(pair):
                for j, feature in enumerate(document.shingles()):
                    pair_lengths[i] += len(feature) * self.feature_weights[j]
            max_similarity = min(pair_lengths)
            if similarity / max_similarity >= self.threshhold:
                duplicates.append(pair)

        # Return dupes
        return duplicates



    def duplicates(self):
        return self._jaccard(self._similarity(self._groups(self.features)))


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


    def _tokenize(self, feature):
        if not feature:
            return ''
        else:
            return re.findall(self.reg, feature)


    def _grams(self, feature):

        tokens = self._tokenize(feature)

        if len(tokens) == 0:
            return [[''] * self.width]
        elif len(tokens) < self.width:
            return list(map(list, zip(*[tokens[i:] + [''] * i for i in range(self.width)])))
        else:
            return list(map(list, zip(*[tokens[i:] for i in range(self.width)])))


    def shingles(self):
        shingle_matrix = []
        
        for feature in self.features:
            if feature == None:
                shingle_matrix.append([])
                continue
            tokens = self._grams(feature)
            shingle_matrix.append(list(map(lambda x: Fingerprint(self.id, tuple(x)), tokens)))

        return shingle_matrix



class Fingerprint(object):


    def __init__(self, doc_id, token):
        self.id = doc_id

        self.token = token
        if self.token == False:
            self.token = None

        self.value = hash(token)


    def __repr__(self):
        return "<Fingerprint: %s>" % (self.id)