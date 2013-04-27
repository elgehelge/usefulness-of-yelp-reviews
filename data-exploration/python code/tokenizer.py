from nltk.tokenize import word_tokenize
from nltk import regexp_tokenize
import re

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
        #if (pattern_numbers.search(word) is not None):
        #        print word
        # Prices
        if '$' in word:
                word = '<PRICE>'
        # Time
        if 'am' in word or 'pm' in word:
                word = '<TIME>'
        # Websites: Look for "www.yelp.com/biz_photos"
        if (pattern_photo.search(word) is not None):
                word = 'www.yelp.com/biz_photos'
        # Repeated letteeeers: Cut 4+ repeated letters down to 3
        repeat_matches = pattern_repeat.finditer(word)
        for m in repeat_matches:
                start = m.span()[0]
                word = word[start:start+3]
        return word


def tokenize(text):
    tokenized = custom_word_tokenization(text)
    return [transform_word(word) for word in tokenized]
