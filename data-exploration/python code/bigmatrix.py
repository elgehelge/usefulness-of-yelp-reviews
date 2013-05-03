from load_json import *
from sklearn.feature_extraction import DictVectorizer

business, checkin, review, user = get_data()

for i, r in enumerate(review):
    # Rearrenge votes
    r[u'votes_useful'] = r['votes']['useful']
    r[u'votes_funny'] = r['votes']['funny']
    r[u'votes_cool'] = r['votes']['cool']
    del r['votes']

v = DictVectorizer(sparse=True)
X = v.fit_transform(review)

print X