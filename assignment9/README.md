# Comparing Postgres and Neo4j

The description of this exercise, datasets and instructions can be found [here](https://github.com/datsoftlyngby/soft2018spring-databases-teaching-material/blob/master/assignments/Neo4J%20Exercise.ipynb).

## Set up and populate a PostgreSQL database
1. Install PostgreSQL
Using a local version of Postgresql from [Postgres.app – the easiest way to get started with PostgreSQL on the Mac](https://postgresapp.com/)
2. Create a DB in the GUI and open the CLI for executing psql commands
3. Create a table for nodes

```sql
CREATE TABLE nodes
(
  id serial NOT NULL,
  name character varying(200),
  job character varying(200),
  birthday date,
  CONSTRAINT nodes_pkey PRIMARY KEY (id)
);
```

4. Import the nodes from the respective .csv file
```sql
COPY nodes(id,name,job,birthday) 
FROM '/Users/edmondpetres/Desktop/archive_graph/social_network_nodes.csv' DELIMITER ',' CSV HEADER;
```

5. Create the table for the edges
```sql
CREATE TABLE edges
(
  source BIGINT,
	target BIGINT
);
```

6. Import the edges into it’s table
```sql
COPY edges(source,target) 
FROM '/Users/edmondpetres/Desktop/archive_graph/social_network_edges.csv' DELIMITER ',' CSV HEADER;
```

## Set up and populate Neo4j database
1. Download and install the Neo4j desktop app
2. Create a graph (called `comparison-exercise` with password `secret`)
3. Place the csv files that need to be imported in the import folder of Neo4j. Mine was here on Mac: 
`/Users/edmondpetres/Library/Application Support/Neo4j Desktop/Application/neo4jDatabases/database-6d29e703-c4f3-4d7e-a09b-1f270ee983a7/installation-3.4.0/import`
4. Add this settings to neo4j db configuration:
```
dbms.security.allow_csv_import_from_file_urls=true
dbms.directories.import=import
```
6. Import the Nodes with the following command:
```cypher
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///archive_graph/social_network_nodes.csv" AS row
CREATE (:Nodes {id: row.node_id, name: row.name, job: row.job, birthday: row.birthday});
```
7. Import the edges
```
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///archive_graph/social_network_edges.csv" AS row
CREATE (:Edges {source: row.source_node_id, target: row.target_node_id});
```
8. 

### SQL queries 

Depth 1
```sql
SELECT * FROM nodes WHERE id IN 
(SELECT source FROM edges WHERE target = 3);
```

Depth 2
```sql
SELECT * FROM nodes WHERE id IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source = 5));
```

Depth 3
```sql 
SELECT * FROM nodes WHERE node_id IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source = 3)));
```

Depth 4
```sql 
SELECT * FROM nodes WHERE node_id IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source = 3))));
```

Depth 5
```sql 
SELECT * FROM nodes WHERE node_id IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source IN 
(SELECT target FROM edges WHERE source = 3)))));
```

| Query        | Avg SQL           | Median SQL  | Avg Graph | Median Graph | 
| ------------- |-------------| ----- | ----- | ----- |
| Depth 1 | 687ms  |  689ms | 12ms | 7.8ms |
| Depth 2 | 1.7s | 1.7s | 17.6ms | 12.9ms |
| Depth 3 | 2.6s | 2.5s | 201.1ms | 189.3ms |
| Depth 4 | 6s | 5.9s | 3.842s | 3.189s |
| Depth 5 | 11s | 10.7s | 42s | 31s |

## Conclusion

Graph databases, Neo4j in our case has vastly outperformed (in most cases) PostgreSQL when it comes to deeper levels of querying, as the chart above indicates. The lower four levels of queries has bean steadily beaten by a huge margin by the Graph database. On the deeper levels, however, I am wondering if some optimization of the memory usage, or other kind of tweaking could help Neo4j do better than those rather sluggish depth 5 result.

Overall we can say that in this use case, where we want to perform deeper levels of searching in our large datasets, we are much better of choosing a Graph database over an SQL alternative.