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
numberOfFeatures = length(allWords) + 8

# Create empty matrix for user data
i = c(1,numberOfReviews)
j = c(1,numberOfFeatures)
dn <- list(1:numberOfReviews, allWords)
user_matrix = sparseMatrix(i, j, x=c(0,0), dimnames=dn)

metaWords = c("review_id_review", "user_id_review", "business_id_review", "stars_review", "votes_useful_review", "votes_cool_review", "votes_funny_review", "date_review", "type_review")

for(i in 1:10) {
  # Take the meta-data
  user_matrix[i, 1] = data[[1]][i][[1]]$review_id_review
  user_matrix[i, 2] = data[[1]][i][[1]]$user_id_review
  user_matrix[i, 3] = data[[1]][i][[1]]$business_id_review
  user_matrix[i, 4] = data[[1]][i][[1]]$stars_review
  user_matrix[i, 5] = data[[1]][i][[1]]$votes_useful_review
  user_matrix[i, 6] = data[[1]][i][[1]]$votes_cool_review
  user_matrix[i, 7] = data[[1]][i][[1]]$votes_funny_review
  user_matrix[i, 8] = data[[1]][i][[1]]$date_review
  
  # We need a list of all words here
  words = names(data[[1]][i][[1]])
  user_matrix[i, words] = as.numeric(subset(data[[1]][i][[1]], !(names(data[[1]][i][[1]]) %in% metaWords)))
  
  print(paste0("Status ", i, "/", numberOfReviews))
}

writeMM(user_matrix, "/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/reviews_matrix.spm")