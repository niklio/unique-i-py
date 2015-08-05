# -*- coding: utf-8 -*-
import itertools, collections

from docproduct import Docproduct
from document import Document

threshhold = .45

documents = []

query = Docproduct(limit=1000)._query()

for row in query:
    print(row)

# for row in query:
#     document = Document(' '.join(str(i) for i in row))
#     documents.append(document)

# fingerprints = sorted(list(itertools.chain(*[i.features() for i in documents])), key=lambda x: x.value)

# grouped = []

# for k, g in itertools.groupby(fingerprints, lambda x: x.value):
#     g = list(g)
#     if len(g) > 1:
#         grouped.append(g)

# similarity = collections.defaultdict(int)

# for group in grouped:
#     ids = map(lambda x: x.id, group)
#     id_pairs = map(tuple, itertools.permutations(ids, 2))

#     for pair in id_pairs:
#         similarity[pair] += 1

# duplicates = []

# for k, v in similarity.iteritems():
#     pair = map(lambda x: [doc for doc in documents if doc.id == x][0], k)
#     length = sum(map(lambda x: len(x._sketch()), pair))
#     if v / length >= threshhold:
#         duplicates.append(pair)

# for a, b in duplicates:
#     print a.value
#     print b.value
#     print "\n\n"

