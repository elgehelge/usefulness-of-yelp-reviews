# Features to extract:
# --------------------
#
# - Word counts for words that appear 5 times or more in the training set (transformed to lowercase)
# - Count of: ?, !, <PRICE>, <TIME>, <REPEATEEEED>, <UPPERCASE>
# - Average happiness, happiness of most happy and least happy word
# - Length (no of words!) of review
# - LIX number
# - Words per sentence (nltk.WordPunctTokenizer(): http://nltk.googlecode.com/svn/trunk/doc/book/book.html#sentence-segmentation)

# More advanced:
# --------------
# - Ngrams (http://nltk.googlecode.com/svn/trunk/doc/howto/collocations.html)
# - Tagging (http://nltk.googlecode.com/svn/trunk/doc/book/book.html#categorizing-and-tagging-words,   http://nltk.googlecode.com/svn/trunk/doc/book/book.html#search,   https://www.google.dk/search?q=python+automatic+tagging)
# - <NAME> using nltk.corpus.names (http://nltk.googlecode.com/svn/trunk/doc/book/book.html#lexical-resources)
# - <CATEGORY> (like <FOOD> and other categories) using WordNet (automated by looking at a word and clibing up the tree if the depth is above a certain threshold) (http://nltk.googlecode.com/svn/trunk/doc/book/book.html#wordnet)
# - Ngrams of tagging (http://nltk.googlecode.com/svn/trunk/doc/book/book.html#shallow-linguistic-processing,   http://nltk.googlecode.com/svn/trunk/doc/book/ch07.html)
# - Chunks (like on frontpage: http://nltk.org/index.html)
# - Stemming (http://nltk.googlecode.com/svn/trunk/doc/book/book.html#normalizing-text)


from load_json import *
from print_log import *
from tokenizer import *
import pickle
import json

# Enable logging
logging(True)

# Load data
business, checkin, review, user = get_data()
most_common_words = pickle.load(open("most_common_words_count500.pkl"))

# Run through the review list and rearrange each dictionary 
log("Constructing bag-of-words dictionary of reviews")
for i, r in enumerate(review):
    if (i % 1000 == 0):
        log('%i/%i - %i%%' % (i, len(review), float(i)/len(review)*100))
    #if (i == len(review)/10):
    #    break

    # Rearrenge votes
    r[u'votes_useful'] = r['votes']['useful']
    r[u'votes_funny'] = r['votes']['funny']
    r[u'votes_cool'] = r['votes']['cool']
    del r['votes']

    text = r['text']
    tokens = tokenize(r['text'])

    # New features
    r[u'no_of_words'] = len(tokens)
    #r[u'longest_word'] = max([len(word) for word in tokens])
        
    # Rearrange text into bag-of-words
    for word in tokens:
        # Put in dictionary
        word += '_word'
        if word in r:
            r[word] += 1
        else:
            r[word] = 1
    del r['text']

    # Suffix on all keys
    for k in r.keys():
        r[k + '_review'] = r[k]
        del r[k]

size_of_data = sum([len(r) for r in review])
log("Saving json - Data size: %i" % size_of_data)
json.dump(review, open('review_bag_of_words.json','wb'))
# Fixing "Incomplete final line" error in R
f = open('review_bag_of_words10000.json','wb')
f.write('\n')
f.close()
log("json saved")
