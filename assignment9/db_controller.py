import psycopg2
import sys
import pprint
import timeit
from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
import random
import numpy as np
import statistics

db = GraphDatabase("http://localhost:7474", username="neo4j", password="secret")

psql_d1_time = []
psql_d2_time = []
psql_d3_time = []
psql_d4_time = []
psql_d5_time = []

neo4j_d1_times = []
neo4j_d2_times = []
neo4j_d3_times = []
neo4j_d4_times = []
neo4j_d5_times = []

def connect_psql():
  conn_string = "host='localhost' dbname='eddmond' user='postgres' password=''"
  # print the connection string we will use to connect
  print("Connecting to database\n", conn_string)

  # get a connection, if a connect cannot be made an exception will be raised here
  conn = psycopg2.connect(conn_string)

  # conn.cursor will return a cursor object, you can use this cursor to perform queries
  cursor = conn.cursor()

  return cursor

def sql_depth1(node_id = 1):
  cursor = connect_psql()

  # execute our Query
  cursor.execute("SELECT * FROM nodes WHERE id IN (SELECT source FROM edges WHERE target = {});".format(node_id))

  # retrieve the records from the database
  records = cursor.fetchall()
  print('Depth 1: count', len(records))

  # print out the records using pretty print
  # note that the NAMES of the columns are not shown, instead just indexes.
  # for most people this isn't very useful so we'll show you how to return
  # columns as a dictionary (hash) in the next example.
  # pprint.pprint(records)

def sql_depth2 (node_id = 3):
  cursor = connect_psql()

  cursor.execute("""
    SELECT * FROM nodes WHERE id IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source = {}));
    """.format(node_id))
  records = cursor.fetchall()

  print('Depth 2: count', len(records))

def sql_depth3 (node_id = 1):
  cursor = connect_psql()

  cursor.execute("""
    SELECT * FROM nodes WHERE id IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source = {})));
    """.format(node_id))

  records = cursor.fetchall()
  print('Depth 3: count', len(records))

def sql_depth4 (node_id = 1):
  cursor = connect_psql()

  cursor.execute("""
    SELECT * FROM nodes WHERE id IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source = {}))));
    """.format(node_id))

  records = cursor.fetchall()
  print('Depth 4: count', len(records))

def sql_depth5 (node_id = 2):
  cursor = connect_psql()

  cursor.execute("""
    SELECT * FROM nodes WHERE id IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source IN 
    (SELECT target FROM edges WHERE source = 3)))));
    """)

  records = cursor.fetchall()
  pprint.pprint(len(records))

def get_20_random_nodes():
  random_nums = []
  for x in range(20):
    rand_int = random.randint(1,500000)
    random_nums.append(rand_int)
  return random_nums

def run_queries():
  random_nodes = get_20_random_nodes()

  for i in range(len(random_nodes)):
    node_id = random_nodes[i]
    run_psql_nodes(node_id)
    run_neo4j_nodes(node_id)

  calculate_execution_times()

def calculate_execution_times():
  print("PSQL runtimes")
  print("Depth 1 mean:", statistics.median(psql_d1_time))
  print("Average", np.average(psql_d1_time))
  print("Depth 2 mean:", statistics.median(psql_d2_time))
  print("Average", np.average(psql_d2_time))
  print("Depth 3 mean:", statistics.median(psql_d3_time))
  print("Average", np.average(psql_d3_time))
  print("Depth 4 mean:", statistics.median(psql_d4_time))
  print("Average", np.average(psql_d4_time))
  print("Depth 5 mean:", statistics.median(psql_d5_time))
  print("Average", np.average(psql_d5_time))

  print("\nNeo4J runtimes")
  print("Depth 1")
  print("Average", np.average(neo4j_d1_times))
  print("Mean", statistics.median(neo4j_d1_times))
  print("Depth 2")
  print("Average", np.average(neo4j_d2_times))
  print("Mean", statistics.median(neo4j_d2_times))
  print("Depth 3")
  print("Average", np.average(neo4j_d3_times))
  print("Mean", statistics.median(neo4j_d3_times))
  print("Depth 4")
  print("Average", np.average(neo4j_d4_times))
  print("Mean", statistics.median(neo4j_d4_times))
  print("Depth 5")
  print("Average", np.average(neo4j_d5_times))
  print("Mean", statistics.median(neo4j_d5_times))

def run_psql_nodes(node_id):
  start = timeit.default_timer()
  sql_depth1(node_id)
  stop = timeit.default_timer()
  execution_time_d1 = stop - start
  print('Execution time SQL depth 1:', execution_time_d1)
  psql_d1_time.append(execution_time_d1)
  
  start = timeit.default_timer()
  sql_depth2(node_id)
  stop = timeit.default_timer()
  execution_time_d2 = stop - start
  print('Execution time SQL depth 2:', execution_time_d2)
  psql_d2_time.append(execution_time_d2)

  start = timeit.default_timer()
  sql_depth3()node_id
  stop = timeit.default_timer()
  execution_time_d3 = stop - start
  print('Execution time SQL depth 3:', execution_time_d3)
  psql_d3_time.append(execution_time_d3)

  start = timeit.default_timer()
  sql_depth4(node_id)
  stop = timeit.default_timer()
  execution_time_d4 = stop - start
  print('Execution time SQL depth 4:', execution_time_d4)
  psql_d4_time.append(execution_time_d4)

  start = timeit.default_timer()
  sql_depth5(node_id)
  stop = timeit.default_timer()
  execution_time_d5 = stop - start
  print('Execution time SQL depth 5:', execution_time_d5)
  psql_d5_time.append(execution_time_d5)


def run_neo4j_nodes(node_id):
  start = timeit.default_timer()
  sql_depth1(node_id)
  stop = timeit.default_timer()
  execution_time_d1 = stop - start
  print('Execution time neo4j depth 1', execution_time_d1)
  neo4j_d1_times.append(execution_time_d1)
  
  start = timeit.default_timer()
  sql_depth2(node_id)
  stop = timeit.default_timer()
  execution_time_d2 = stop - start
  print('Execution time neo4j depth 2', execution_time_d2)
  neo4j_d2_times.append(execution_time_d2)
  
  start = timeit.default_timer()
  sql_depth3(node_id)
  stop = timeit.default_timer()
  execution_time_d3 = stop - start
  print('Execution time neo4j depth 3', execution_time_d3)
  neo4j_d3_times.append(execution_time_d3)
  
  start = timeit.default_timer()
  sql_depth4(node_id)
  stop = timeit.default_timer()
  execution_time_d4 = stop - start
  print('Execution time neo4j depth 4', execution_time_d4)
  neo4j_d4_times.append(execution_time_d4)
  
  start = timeit.default_timer()
  sql_dept5(node_id)
  stop = timeit.default_timer()
  execution_time_d5 = stop - start
  print('Execution time neo4j depth 5', execution_time_d5)
  neo4j_d5_times.append(execution_time_d5)


# Neo4j queries
def neo4j_depth1(node_id = 1):
  query = 'MATCH (x:Person)-[:ENDORSES]->(other) WHERE ID(x)= {} return DISTINCT ID(other), other.name, other.job, other.birthday'.format(node_id)
  
  results = db.query(query, returns=(client.Node, str, client.Node))
  print('Results length:', len(results))
  
def neo4j_depth2(node_id = 1):
  query = 'MATCH (x:Person)-[:ENDORSES]->()-[:ENDORSES]->(other) WHERE ID(x)= {} return DISTINCT ID(other), other.name, other.job, other.birthday'.format(node_id)
  
  results = db.query(query, returns=(client.Node, str, client.Node))
  print('Results length:', len(results))
  
def neo4j_depth3(node_id = 1):
  query = 'MATCH (x:Person)-[:ENDORSES]->()-[:ENDORSES]->()-[:ENDORSES]->(other) WHERE ID(x)= {} return DISTINCT ID(other), other.name, other.job, other.birthday'.format(node_id)
  
  results = db.query(query, returns=(client.Node, str, client.Node))
  print('Results length:', len(results))
  
def neo4j_depth4(node_id = 1):
  query = 'MATCH (x:Person)-[:ENDORSES]->()-[:ENDORSES]->()-[:ENDORSES]->()-[:ENDORSES]->(other) WHERE ID(x)= {} return DISTINCT ID(other), other.name, other.job, other.birthday'.format(node_id)
  
  results = db.query(query, returns=(client.Node, str, client.Node))
  print('Results length:', len(results))
  
def neo4j_depth5(node_id = 1):
  query = 'MATCH (x:Person)-[:ENDORSES]->()-[:ENDORSES]->()-[:ENDORSES]->()-[:ENDORSES]->()-[:ENDORSES]->(other) WHERE ID(x)= {} return DISTINCT ID(other), other.name, other.job, other.birthday'.format(node_id)
  
  results = db.query(query, returns=(client.Node, str, client.Node))
  print('Results length:', len(results))



if __name__ == "__main__":
  run_queries()