import json

# Define file path and file names

file_path = 'yelp-data/yelp_training_set/'

file_name_business = 'yelp_training_set_business.json'
file_name_checkin = 'yelp_training_set_checkin.json'
file_name_review = 'yelp_training_set_review.json'
file_name_user = 'yelp_training_set_user.json'


# Read data and convert to objects

def read_data(file_name):
    content = open(file_path + file_name, 'rb').read()
    list_of_strings = content.split('\r\n')[:-1]
    list_of_json = [json.loads(string) for string in list_of_strings]
    return list_of_objects

def get_data():
    business = get_data(file_name_business)
    checkin = get_data(file_name_checkin)
    review = get_data(file_name_review)
    user = get_data(file_name_user)
    return business, checkin, review, user
