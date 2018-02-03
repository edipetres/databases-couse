import random
import string
import timeit

def generate_random_date():
  chars = string.ascii_letters + string.digits
  return ''.join(random.sample(chars, 5))

list_len = 10
simple_index = {el: generate_random_date() for el in range(list_len)}
print simple_index



