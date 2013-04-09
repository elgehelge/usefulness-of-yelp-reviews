from nltk.tokenize import word_tokenize
from load_json import *
from print_log import *

# Enable logging
logging(True)

# Load data
business, checkin, review, user = get_data()

# Run through all review and construct a dictionary of all words
all_words = {}
for i, r in enumerate(review):
	if (i % 1000 == 0):
		log('%i/%i - %i%%' % (i, len(review), float(i)/len(review)*100))
	for word in word_tokenize(r['text']):
		all_words[word] = True
