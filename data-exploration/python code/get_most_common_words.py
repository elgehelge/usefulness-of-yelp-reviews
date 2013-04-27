from load_json import *
from print_log import *
from tokenizer import *

# Enable logging
logging(True)

# Load data
business, checkin, review, user = get_data()

# Run through all reviews and construct a dictionary of all words
print "Constructing dictionary of all words"
all_words = {}
for i, r in enumerate(review):
    if (i % 1000 == 0):
            log('%i/%i - %i%%' % (i, len(review), float(i)/len(review)*100))
    for word in tokenize(r['text']):
            word = transform_word(word)
            # Put in dictionary
            if word in all_words:
                    all_words[word] += 1
            else:
                    all_words[word] = 1

print "Finding most common words"
most_common_words = {}
for i in all_words.items():
        word = i[0]
        count = i[1]
        if count >= 5:
                most_common_words[word] = count
