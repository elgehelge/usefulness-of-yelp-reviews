library("rjson")

json_file = "/Users/utdiscant/github/usefulness-of-yelp-reviews/yelp-data/yelp_training_set/yelp_training_set_user.json"

contents = readLines(json_file)
data = lapply(contents, fromJSON)

# Create empty matrix for user data
user_matrix = matrix(0, length(data), 8)

for(i in 1:length(data)) {
  user_matrix[i, 1] = data[[i]]$user_id
  user_matrix[i, 2] = data[[i]]$name
  user_matrix[i, 3] = data[[i]]$review_count
  user_matrix[i, 4] = data[[i]]$average_stars
  user_matrix[i, 5] = data[[i]]$type
  user_matrix[i, 6] = data[[i]]$votes$funny
  user_matrix[i, 7] = data[[i]]$votes$cool
  user_matrix[i, 8] = data[[i]]$votes$useful
}

user_df = as.data.frame(user_matrix)
names(user_df) = c("user_id", "name", "review_count", "average_stars", "type", "votes_funny", "votes_cool", "votes_useful")