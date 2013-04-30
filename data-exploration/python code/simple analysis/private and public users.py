from load_json import *
from print_log import *
from tokenizer import *
import pickle
import json

# Enable logging
logging(True)

# Load data
business, checkin, review, user = get_data()
most_common_words = pickle.load(open("../data/43176_most_common_words.pkl"))

# Users vs reviews
>>> user_ids = {}
>>> for u in user:
	user_ids[u['user_id']] = True
>>> len(user_ids)
43873

>>> review_user_ids = {}
>>> for u in review:
	review_user_ids[u['user_id']] = True
>>> len(review_user_ids)
45981

>>> diff = set(user_ids.keys()).difference(set(review_user_ids.keys()))
>>> len(diff)
0

>>> diff = set(review_user_ids.keys()).difference(set(user_ids.keys()))
>>> len(diff)
2108

>>> sum([1 for r in review if r['user_id'] in diff])
14028

>>> useful_sum_private = 0
>>> useful_sum_public = 0
>>> count_private = 0
>>> count_public = 0
>>> for r in review:
	if r['user_id'] in diff:
		count_private += 1
		useful_sum_private += r['votes']['useful']
	else:
                count_public += 1
                useful_sum_public += r['votes']['useful']
>>> float(useful_sum) / count
