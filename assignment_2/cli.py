import pymongo
from pymongo import MongoClient
from pprint import pprint
import operator

client = MongoClient()
db = client.social_net

def get_distinct_users():
  return len(db.tweets.distinct('user'))

def get_most_linked_users(query_limit=0, results_limit=10):
  users_dict = {}
  
  for doc in db.tweets.find({}).limit(query_limit):
    if "@" in doc['text']:
      text = doc['text']
      linked_user = text[text.find('@')+1:text.find(' ')]
      if linked_user == "":
        pass
      elif linked_user not in users_dict:
        users_dict[linked_user] = 1
      else:
        users_dict[linked_user] += 1
  
  sorted_users = sorted(users_dict.items(), key=operator.itemgetter(1), reverse=True)
  return sorted_users[:results_limit]

def get_most_active_users(query_limit=10000, results_limit=10):
  users_dict = {}
  
  for doc in db.tweets.find({}).limit(query_limit):
    user = doc['user']
    if user not in users_dict:
      users_dict[user] = 1
    else:
      users_dict[user] += 1
  sorted_users = sorted(users_dict.items(), key=operator.itemgetter(1), reverse=True)
  
  return sorted_users[:results_limit]

# pprint("Most linked twitter users:\n", get_most_linked_users())
# print("Individual twitter users:", get_distinct_users())

most_active_users = get_most_active_users()
print("Most active Twitter users:")
pprint(most_active_users)