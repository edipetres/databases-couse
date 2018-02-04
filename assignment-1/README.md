# Assignment 1 - Simple DB with a Hashmap-based Index

- Build a simple_db in the programming language of your choice.
  - Implement a Hashmap-based index.
  - Implement functionality to store your data on disk in a binary file.
  - Implement functionality to read your data from disk again, so that you can reinstantiate your database after a shutdown.
- Hint: You do not want to serialize and deserialize the an in memory Hashmap containing all data directly. Instead, you in memory index based on a Hashmap contains information on where in you database file a piece of information is stored.