from load_json import *
from print_log import *
from tokenizer import *
from bag_of_words import *
import pickle
import json

# Enable logging
logging(True)

# Load data
# Is already loaded: business, checkin, review, user
stopEarly = True
review = rearrange_review(review, stopEarly)

user_dict = {}
for u in user:
    suffixifyDict(u, '_user')
    user_dict[u[u'user_id_user']] = u
business_dict = {}
for b in business:
    suffixifyDict(b, '_business')
    business_dict[b[u'business_id_business']] = b
checkin_dict = {}
for c in checkin:
    suffixifyDict(c, '_checkin')
    checkin_dict[c[u'business_id_checkin']] = c

# Merge everything into one dictionary
missing_users = 0
missing_businesses = 0
missing_checkins = 0
for r in review:
    user_id = r['user_id_review']
    business_id = r['business_id_review']
    # Merge with users
    if user_id in user_dict:
        r.update(user_dict[user_id])
    else:
        missing_users += 1
    # Merge with businesses
    if business_id in business_dict:
        r.update(business_dict[business_id])
    else:
        missing_businesses += 1
    # Merge with checkins
    if business_id in checkin_dict:
        r.update(checkin_dict[business_id])
    else:
        missing_checkins += 1
print 'Missing users: %s' % missing_users
print 'Missing businesses: %s' % missing_businesses
print 'Missing checkins: %s' % missing_checkins
print 'Big matrix DONE!'

# Restructure features (right now we just remove them instead!)
#Keys containing non-numerical values:
set([u'votes_user', u'date_review', u'checkin_info_checkin', u'categories_business', u'open_business', u'type_business'])

# Remove features
remove_features = [u'neighborhoods_business', u'user_id_review', u'type_user', u'type_review', u'user_id_user', u'type_checkin', u'city_business', u'state_business', u'business_id_business', u'name_user', u'full_address_business', u'review_id_review', u'name_business', u'business_id_checkin', u'business_id_review']
print 'Removing the following features:'
print remove_features
for r in review:
    for f in remove_features:
        if f in r:
            del r[f]

print 'Keys containing non-numerical values:'
nonNumericalKeys = set([item[0] for r in review for item in r.items() if type(item[1]) != int and type(item[1]) != float])
print nonNumericalKeys
