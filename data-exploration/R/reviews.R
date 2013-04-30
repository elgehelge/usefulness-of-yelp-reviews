# Clear memory
rm(list=ls())

library("rjson")
library("Matrix")

json_file = "/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/data/review_bag_of_words_43176.json"
data = lapply(readLines(json_file), fromJSON)
numberOfReviews = length(data[[1]])

# Get words
wordlist_file = "/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/data/43176_most_common_words.pkl"
wordList = readLines(wordlist_file)
words = wordList[seq(from = 5, to = length(wordList), by = 3)]
allWords = as.character(lapply(words, function(x) substr(x,3,nchar(x))))

# Business_id, stars_review, votes_cool_review, votes_useful_review, votes_funny_review, review_id_review, date_review, type_review, user_id_review
# We ignore the variable "type_review"
numberOfFeatures = length(allWords) + 9

metaWords = c("review_id_review", "user_id_review", "business_id_review", "stars_review", "votes_useful_review", "votes_cool_review", "votes_funny_review", "date_review", "no_of_words_review", "type_review")

# Create empty matrix for user data
i = c(1,numberOfReviews)
j = c(1,numberOfFeatures)
dn <- list(1:numberOfReviews, c(metaWords[1:9], allWords))
user_matrix = sparseMatrix(i, j, x=c(0,0), dimnames=dn)


# We can not store the id-strings in the sparse matrix, so we just store numbers 1 to numberOfReviews
review_ids = list()
user_ids = list()
business_ids = list()
dates = list()

for(i in 1:10) {
  review_ids = c(review_ids, data[[1]][i][[1]]$review_id_review)
  user_ids = c(user_ids, data[[1]][i][[1]]$user_id_review)
  business_ids = c(business_ids, data[[1]][i][[1]]$business_id_review)
  
  user_matrix[i, metaWords[1]] = i
  user_matrix[i, metaWords[2]] = i
  user_matrix[i, metaWords[3]] = i
  user_matrix[i, metaWords[4]] = data[[1]][i][[1]]$stars_review
  user_matrix[i, metaWords[5]] = data[[1]][i][[1]]$votes_useful_review
  user_matrix[i, metaWords[6]] = data[[1]][i][[1]]$votes_cool_review
  user_matrix[i, metaWords[7]] = data[[1]][i][[1]]$votes_funny_review
  
  dates = c(dates, data[[1]][i][[1]]$date_review)
  user_matrix[i, metaWords[8]] = i
  
  user_matrix[i, metaWords[9]] = data[[1]][i][[1]]$no_of_words_review
  
  for(w in names(data[[1]][i][[1]])) {
    if(!(w %in% metaWords)) {
      word = substr(w, 1, nchar(w)-12)
      print(w)
      print(word)
      print(i)
      user_matrix[i, word] = as.numeric(data[[1]][i][[1]][w])
    }
  }
  
  print(paste0("Status ", i, "/", numberOfReviews))
}

writeMM(user_matrix, "/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/reviews_matrix.spm")