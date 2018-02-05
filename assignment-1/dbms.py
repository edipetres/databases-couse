import random
import string
import sys

index_store = {}
db_filename = 'py_database'
index_filename = 'py_index'

def write(key, value):
  with open(db_filename, 'a') as db:
    key = str(key)
    value = str(value)
    line = key + ':' + value + '\n'
    index_new_key(key)
    db.writelines(line)
    db.flush()

def read(key):
  read_index_from_file()
  value = ''
  with open(db_filename, "r") as f:
    key_index = index_store.get(key) or 0
    key_index = int(key_index)
    f.seek(key_index)
    line = f.readline().strip()
    value = line.split(':')[1]
  return value

def index_new_key(key):
  read_index_from_file()
  with open(db_filename, 'r') as f:
    file_content = f.read()
    index = file_content.rfind('\n' + key + ':')
    if not index == -1:
      index_store[key] = index + 1 # to reflect the one extra EOL character
  write_index_to_file()

def read_index_from_file():
  with open(index_filename, 'rb') as f:
    binary_content = f.read()
    string_content = text_from_bits(binary_content)
    string_content = string_content.split('\n')
    for line in string_content:
      elem_array = line.split(':')
      if len(elem_array) == 2:
        key = elem_array[0]
        value = elem_array[1]
        # print('key:', key, ' | value:', value)
        index_store[key] = value
    # print('Done reading index.')

def write_index_to_file():
  index_stringified = ''
  for key in index_store.keys():
    value = index_store[key]
    index_stringified += '{}:{}\n'.format(key, value)
  index_binary = text_to_bits(index_stringified)
  with open(index_filename, 'wb') as f:
    f.write(index_binary.encode())
    f.flush()

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def generate_random_data():
    chars = string.ascii_letters + string.digits
    return ''.join(random.sample(chars, 5))

# generate random data to populate database
for el in range(10):
  write(el, generate_random_data())

print("index hashmap", index_store)

# ---------------------- REVIEWER --------------------------------
# READ DATA HERE BY KEY:
my_key = 3
print('Read from DB:', read(my_key))
# ---------------------- REVIEWER --------------------------------




# IGNORE: useful scripts
# byte_string = ' '.join(format(ord(x), 'b') for x in line)
# bin_string = bin(int.from_bytes(line.encode(), 'big'))