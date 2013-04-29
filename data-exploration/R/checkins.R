# Clear memory
rm(list=ls())

library("rjson")
library("gdata")

json_file = "/Users/utdiscant/github/usefulness-of-yelp-reviews/yelp-data/yelp_training_set/yelp_training_set_checkin.json"

contents = readLines(json_file)
data = lapply(contents, fromJSON)

numvars = 1 + 24*7

# Create empty matrix for checkin data
checkin_matrix = matrix(0, length(data), numvars)
checkin_df = as.data.frame(checkin_matrix)

time_names = list()
for(fromhour in 0:23) {
  for(dayinweek in 0:6) {
    time_names = c(time_names, paste0(fromhour,"-",dayinweek))
  }
}
time_names = as.character(time_names)

names(checkin_df) = c("id_business", time_names)


for(i in 1:length(data)) {
  checkin_df[i, "id_business"] = data[[i]]$business_id
  
  print(paste0(i, " of ", length(data)))
  
  existing_times = names(data[[i]]$checkin_info)
  checkin_df[i, existing_times] = data[[i]]$checkin_info[existing_times]
}

confun_chtime = function(x) paste0("t",x,"_chtime")

names(checkin_df) = c("id_business", lapply(time_names, confun_chtime))

write.csv(checkin_df, "/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/R/checkin_matrix.csv")