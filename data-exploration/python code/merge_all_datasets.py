from load_json import *
from print_log import *
from tokenizer import *
from bag_of_words import *
from datetime import datetime
from scipy.sparse import csr_matrix
from scipy.io import mmread, mmwrite
from sklearn.feature_extraction import DictVectorizer

# Enable logging
logging(True)

# Load data
# Is already loaded: business, checkin, review, user
stopEarly = False
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

#Keys containing non-numerical values:
#set([u'date_review', , ])


def binarize(dictionary, keyname):
    for k in dictionary.keys():
        dictionary[k][keyname] = int(dictionary[k][keyname])


def unfold(dictionary, keyname):
    for k in dictionary.keys():
        dict_to_unfold = dictionary[k][keyname]
        for sub in dict_to_unfold.keys():
            dictionary[k][keyname + sub] = dict_to_unfold[sub]

        del dictionary[k][keyname]


def uncategorize(dictionary, keyname):
    for k in dictionary.keys():
        for cat in dictionary[k][keyname]:
            dictionary[k][keyname + '_' + cat] = int(True)
        del dictionary[k][keyname]


def datetotime(myList):
    now = datetime.strptime('2013-01-19', '%Y-%m-%d')
    for k in myList:
        date = datetime.strptime(k[u'date_review'], '%Y-%m-%d')
        days = (now-date).days
        k[u'days_review'] = days
        del k[u'date_review']


binarize(business_dict, u'open_business')

unfold(user_dict, u'votes_user')
unfold(checkin_dict, u'checkin_info_checkin')

uncategorize(business_dict, u'categories_business')
uncategorize(business_dict, u'city_business')

datetotime(review)

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
print 'Dictionaries merged'


# Remove features
remove_features = [u'neighborhoods_business', u'user_id_review', u'type_user', u'type_review', u'user_id_user', u'type_checkin', u'state_business', u'business_id_business', u'name_user', u'full_address_business', u'review_id_review', u'name_business', u'business_id_checkin', u'business_id_review', u'type_business']
print 'Removing the following features:'
print remove_features
for r in review:
    for f in remove_features:
        if f in r:
            del r[f]

print "Converting dictionaries to sparse matrix"

v = DictVectorizer(sparse=True)
X = v.fit_transform(review)

print "Writing matrix to disk"

mmwrite('finalMatrix.mtx', X)
# B = mmread('finalMatrix.mtx')
