# -*- coding: utf-8 -*-
import itertools, collections, uuid

from docproduct import Docproduct
from document import Document

def find_duplicates(query, feature_weights, threshhold=.9):

    number_of_features = len(feature_weights)

    documents = {}
    for row in query:
        doc_id = uuid.uuid4()
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

    similarity = collections.defaultdict(lambda:0)
    for i, feature in enumerate(grouped):
        for group in feature:
            ids = [fingerprint.id for fingerprint in group]
            if len(set(ids)) == 1:
                continue
            pairs = list(itertools.combinations(ids, 2))
            for pair in pairs:
                similarity[tuple(sorted(pair))] += feature_weights[i]

    duplicates = []
    for id_pair, similarity in similarity.items():
        pair = [documents[doc_id] for doc_id in id_pair]
        pair_lengths = [0, 0]
        for i, document in enumerate(pair):
            for j, feature in enumerate(document.shingles()):
                pair_lengths[i] += len(feature) * feature_weights[j]
        max_similarity = min(pair_lengths)
        if similarity / max_similarity >= threshhold:
            duplicates.append(pair)

    return duplicates

if __name__ == "__main__":
    query = Docproduct()._query()
    duplicates = find_duplicates(query, [10, 1], threshhold=0.5)
    for a, b in duplicates:
        print(a.features)
        print(b.features)
        print("\n")
