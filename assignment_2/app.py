from __future__ import division
import os
import time
from pymongo import MongoClient
from pprint import pprint
import operator
import re

client = MongoClient()
db = client.social_net

def get_distinct_users():
  users_len = len(db.tweets.distinct('user'))
  print("\n1. Individual twitter users:", users_len, '\n')

def get_mention_stats(query_limit=10000, results_limit=10):
  mentioned_users = {}
  linkers_dict = {}
  
  for doc in db.tweets.find({}).limit(query_limit):
    if "@" in doc['text']:
      text = doc['text']
      user = doc['user']

      # Find how many users a person mentions in their tweets
      linked_users = re.findall('@([A-Za-z0-9_]+)', text)
      if user not in linkers_dict:
        linkers_dict[user] = len(linked_users)
      else:
        linkers_dict[user] += len(linked_users)

      # Find how many times a user was mentioned
      for user in linked_users:
        if user not in mentioned_users:
          mentioned_users[user] = 1
        else:
          mentioned_users[user] += 1
  
  sorted_mentions = sorted(mentioned_users.items(), key=operator.itemgetter(1), reverse=True)
  sorted_linkers = sorted(linkers_dict.items(), key=operator.itemgetter(1), reverse=True)
  
  print('2. Users with most links to other users:')
  pprint(sorted_linkers[:10])
  print('\n3. Most mentioned users')
  pprint(sorted_mentions[:5])


def get_most_active_users(query_limit=0, results_limit=10):
  users_dict = {}
  
  for doc in db.tweets.find({}).limit(query_limit):
    user = doc['user']
    if user not in users_dict:
      users_dict[user] = 1
    else:
      users_dict[user] += 1
  
  sorted_users = sorted(users_dict.items(), key=operator.itemgetter(1), reverse=True)
  print('\n4. Most active Twitter users:')
  pprint(sorted_users[:results_limit])

def get_negative_words():
  words_dic = []
  with open('utils/negative_words.txt', 'r') as f:
    for line in f.readlines():
      # remove lines with comments and empty ones
      if line.startswith(';') or line.startswith('\n'):
        pass
      else:
        words_dic.append(line.rstrip())
  return words_dic

def get_positive_words():
  words = []
  with open('utils/positive_words.txt', 'r') as f:
    for line in f.readlines():
      words.append(line.rstrip())
  return words

def analyse_sentiments(query_limit=0):
  positive_words = get_positive_words()
  negative_words = get_negative_words()
  happy_users = {}
  mad_users = {}
  counter = 0

  total_entries = query_limit if query_limit != 0 else 1600000
  start_time = time.time()
  for doc in db.tweets.find({}).limit(query_limit):
    counter += 1
    if counter % 10000 == 0:
      elapsed_time = time.time() - start_time
      print_stats(counter, total_entries, elapsed_time)
    
    user = doc['user']
    words_array = doc['text'].split(' ')

    for word in words_array:
      if word in negative_words:
        if user in mad_users:
          mad_users[user] += 1
        else:
          mad_users[user] = 1
      elif word in positive_words:
        if user in happy_users:
          happy_users[user] += 1
        else:
          happy_users[user] = 1
  
  mad_sorted = sorted(mad_users.items(), key=operator.itemgetter(1), reverse=True)
  happy_sorted = sorted(happy_users.items(), key=operator.itemgetter(1), reverse=True)
  
  print("\n\nTop 5 happy users (positive words found):")
  pprint(happy_sorted[:5])

  print("\nTop 5 mad users (negative words found):")
  pprint(mad_sorted[:5])

def print_stats(counter, total_entries, time_elapsed):
  os.system('clear')

  percentage = counter * 100 / total_entries
  one_percent = time_elapsed / percentage
  time_remaining = (100 - percentage) * one_percent
  
  if percentage < 1:
    time_remaining_formatted = "Calculating time remaining..."
  else:
    time_remaining_formatted = time.strftime('%H:%M:%S', time.gmtime(time_remaining))
  
  print("Analysing dataset...\n{} %\neta: {}".format(percentage, time_remaining_formatted))


analyse_sentiments()
get_distinct_users()
get_mention_stats()
get_most_active_users()
