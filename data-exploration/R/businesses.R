# Clear memory
rm(list=ls())

library("rjson")
library("gdata")

json_file = "/Users/utdiscant/github/usefulness-of-yelp-reviews/yelp-data/yelp_training_set/yelp_training_set_business.json"

contents = readLines(json_file)
data = lapply(contents, fromJSON)

# Determine the names of all categories
all_categories = list()
for(i in 1:length(data)) {
  all_categories = c(all_categories, data[[i]]$categories)
}
all_categories_names = unique(all_categories)


# Determine the names of all cities
all_cities = list()
for(i in 1:length(data)) {
  all_cities = c(all_cities, trim(data[[i]]$city))
}
all_city_names = unique(all_cities)


# Create empty matrix for business data
business_matrix = matrix(0, length(data), 7+length(all_categories_names)+length(all_city_names))


for(i in 1:length(data)) {
  print(i)
  business_matrix[i, 1] = data[[i]]$business_id
  
  # Ignore adress
  
  business_matrix[i, 2] = data[[i]]$open
  business_matrix[i, 3] = data[[i]]$review_count
  business_matrix[i, 4] = data[[i]]$name
  
  # We ignore the neighborhoods variable
  
  if(is.null(data[[i]]$longitude)) {
    business_matrix[i, 5] = NA
  } else {
    business_matrix[i, 5] = data[[i]]$longitude
  }
  
  if(is.null(data[[i]]$latitude)) {
    business_matrix[i, 6] = NA
  } else {
    business_matrix[i, 6] = data[[i]]$latitude
  }
  
  business_matrix[i, 7] = data[[i]]$stars
  
  # Ignore state
  
  # Now we take care of the category variable
  for(j in 1:length(all_categories_names)) {
    # Determine if category j is on this business
    if(all_categories_names[j] %in% data[[i]]$categories) {
      business_matrix[i, j+8] = 1
    } else {
      business_matrix[i, j+8] = 0
    }
  }
  
  # Now we take care of the city variable
  for(j in 1:length(all_city_names)) {
    # Determine if category j is on this business
    if(all_city_names[j] == trim(data[[i]]$city)) {
      business_matrix[i, j+7+length(all_categories_names)] = 1
    } else {
      business_matrix[i, j+7+length(all_categories_names)] = 0
    }
  }
}
business_matrix[,8:dim(business_matrix)[2]] = apply(business_matrix[,8:dim(business_matrix)[2]],1,as.numeric)

business_df = as.data.frame(business_matrix)

business_df[,8:dim(business_df)[2]] = apply(business_df[,8:dim(business_df)[2]],1,as.numeric)

# Create a list of the normal column names (without the categories)
colNames = c("id_business", "open_business", "review_count_business", "name_business", "longitude_business", "latitude_business", "stars_business")

concfun_cate = function(x) paste0(x,"_cat")
concfun_city = function(x) paste0(x,"_city")

# Add a name for each category
names(business_df) = c(colNames, lapply(all_categories_names,concfun_cate), lapply(all_city_names,concfun_city))

write.csv(business_df, "/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/R/business_matrix.csv")
