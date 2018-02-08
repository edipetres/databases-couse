# CouchDB

Run a CouchDB instance locally
'docker run -d -p 5984:5984 --name couchdbms couchdb'

Access the CouchDB Dashboard in the browser
`localhost:5984/_utils`

## Databases

Get all databases

```sh
> curl -X GET localhost:5984/_all_dbs
["baseball","firstdb","verifytestdb"]
```

Create a database called `Plankton`

```sh
> curl -X PUT localhost:5984/plankton
{"ok":true}
```

## CRUD

Insert a new document

```sh
curl -X PUT localhost:5984/firstdb/myid -d @mylibrary.json

# insert into "firstdb" database
# add document with id "myid"
# -d @mylibrary.json   - use json document from disk
```

```json
// mylibrary.json
{
  "_id": "_design/mylibrary",
  "language": "javascript",
  "views": {
    "books_by_isbn": {
      "map": "function (doc) { if(doc.ISBN) { emit (doc.ISBN, doc); } }"
    },
    "test": true
  }
}
```