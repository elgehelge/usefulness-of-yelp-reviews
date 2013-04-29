# Clear memory
rm(list=ls())

checkins = read.csv("/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/R/checkin_matrix.csv")
checkins = checkins[,2:dim(checkins)[2]]

businesses = read.csv("/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/R/business_matrix.csv")
businesses = businesses[,2:dim(businesses)[2]]

users = read.csv("/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/R/user_matrix.csv")
users = users[,2:dim(users)[2]]

reviews = read.csv("/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/R/")
reviews = reviews[,2:dim(reviews)[2]]

### Join "businesses" and "checkins" on the business id
checkin_and_business = merge(checkins, businesses, by="id_business", all.y=TRUE)

# Convert NA to 0 (we know there is no NA values in either of the two matrices before merging)
checkin_and_business[is.na(checkin_and_business)] = 0



### Make a many to one join of users and reviews




### Make a many to one join of businesses and reviews
