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
 

from nltk.tokenize import word_tokenize
from load_json import *
from print_log import *
from nltk import regexp_tokenize
import re

# Enable logging
logging(True)

# Load data
business, checkin, review, user = get_data()

def custom_word_tokenization(text):
    tokenizierRegex = r'''(?x) # set flag to allow verbose regexps
        ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
      | \w+(-\w+)*        # words with optional internal hyphens
      | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
      | \!+               # !+
      | \?+               # ?+
      | \.+               # .+
      | [][.,;"'?():-_`]  # these are separate tokens
    '''
    return regexp_tokenize(text, tokenizierRegex)

def transform_word(word):
        pattern_photo = re.compile(r'[.]*www\.yelp\.com\/biz\_photos[.*]')
        pattern_repeat = re.compile(r'([\S])\1\1\1+')
        pattern_numbers = re.compile(r'\$?\d+(\.\d+)?%?')
        # Caps: Make lowercase unless the word is ALLCAPS
        if (word != word.upper()):
                word = word.lower()
        # Numbers
        if (pattern_numbers.search(word) != None):
                print word
        # Prices
        if '$' in word:
                word = '<PRICE>'
        # Time
        if 'am' or 'pm' in word:
                word = '<TIME>'
        # Websites: Look for "www.yelp.com/biz_photos"
        if (pattern_photo.search(word) != None):
                word = 'www.yelp.com/biz_photos'
        # Repeated letteeeers: Cut 4+ repeated letters down to 3
        repeat_matches = pattern_repeat.finditer(word)
        for m in repeat_matches:
                start = m.span()[0]
                word = word[start:start+3]
        return word

# Run through all review and construct a dictionary of all words
all_words = {}
for i, r in enumerate(review):
        if (i % 1000 == 0):
                log('%i/%i - %i%%' % (i, len(review), float(i)/len(review)*100))
        for word in custom_word_tokenization(r['text']):
                word = transform_word(word)
                # Put in dictionary
                if word in all_words:
                        all_words[word] += 1
                else:
                        all_words[word] = 1

most_common_words = {}
for i in all_words.items():
        word = i[0]
        count = i[1]
        if count >= 5:
                most_common_words[word] = count
