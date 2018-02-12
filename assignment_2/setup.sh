# Getting started
# Run this script to download the dataset and populate your Mongo database

# extract training data
unzip utils/trainingdata.zip -d utils

# run mongodb instance on localhost
docker run --rm -v $(pwd)/data:/data/db --publish=27017:27017 --name dbms -d mongo

# import dataset into our local database
mongoimport --drop --db social_net --collection tweets --type csv --headerline --file utils/training.1600000.processed.noemoticon.csv

# run the python analysis
python3 app.py