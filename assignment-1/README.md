# Assignment 1 - Simple DB with a Hashmap-based Index

## Requirements

- Build a simple_db in the programming language of your choice.
  - Implement a Hashmap-based index.
  - Implement functionality to store your data on disk in a binary file.
  - Implement functionality to read your data from disk again, so that you can reinstantiate your database after a shutdown.
- Hint: You do not want to serialize and deserialize the an in memory Hashmap containing all data directly. Instead, you in memory index based on a Hashmap contains information on where in you database file a piece of information is stored.

## Start here [Solution]

### JavaScript

I have made attempts to creat the Database Management System in JavaScript, but I failed miserably. It is the wrong tool for dealing with binary I/O. If you do want to have a look at it it's in the `/failed_trial` folder.

### Python

To use the database management system run the main file:

```sh
python3 dbms.py
```

Running the file will populate the database with random data and read back the value for key `3`. Running the file multiple times will add new data to the database with the same keys (0 -> 9) and hence you can see the index file updating and that the program returns new data for the same key every time.

See the `REVIEWER` section in the python file that you can overwrite to observe different results.

#### Functionality

Data is stored in the `py_database` file. A hash index is being update with the bit offset of the key whenever a new key-value pair is added.

This hashmap is written into the file `py_index` in binary format and read back from file so that the indexing of the database can be reinstantiated when the system restarts.
