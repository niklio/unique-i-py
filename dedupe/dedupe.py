# -*- coding: utf-8 -*-
import itertools, collections

from docproduct import Docproduct
from document import Document

threshhold = .2
feature_weights = [2, 1]
number_of_features = len(feature_weights)

documents = {}
query = Docproduct(limit=1000)._query()
for row in query:
    doc_id = id(row)
    documents[doc_id] = Document(doc_id, row)

# Documents of features of fingerprints
fingerprints = [document.shingles() for document in documents.values()]

assert all([number_of_features == len(fingerprint) for fingerprint in fingerprints])

features = [[] for i in range(number_of_features)]
for document in fingerprints:
    for i, feature in enumerate(document):
        for fingerprints in feature:
            features[i].append(fingerprints)

grouped = [[] for i in range(len(features))]
for i, feature in enumerate(features):
    for key, group in itertools.groupby(feature, lambda x: x.value):
        group = list(group)
        if len(group) > 1:
            grouped[i].append(group)

similarity = collections.defaultdict(lambda:1)
for i, feature in enumerate(grouped):
    feature_similarity = collections.defaultdict(int)
    for group in feature:
        ids = [fingerprint.id for fingerprint in group]
        id_pairs = list(itertools.permutations(ids, 2))
        for id_pair in id_pairs:
            feature_similarity[id_pair] += feature_weights[i]
    for key, value in feature_similarity.items():
        similarity[key] *= value

print(similarity)



