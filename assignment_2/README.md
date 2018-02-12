# Twitter Dataset Analysis

This repository is a self-contained dataset analysis.

## Prerequisites

The following CLI tools are required to run this project:

- docker
- git
- python3

## Getting started

Run the following script from its directory to get started

```sh
sudo ./setup.sh
```

This command will extract the dataset. It spins up a mongo database locally with a data volume mounted to the `data` folder using Docker. Then it populates the database with the extracted dataset. Finally, it runs the Python script to analyse the data and prints out the results.

## Results

The program should output the following results

```sh
Top 5 happy users (positive words found):
[('syarif_m2e', 79),
 ('manatmouse', 76),
 ('Jeff_Hardyfan', 55),
 ('thalovebug', 49),
 ('shanajaca', 42)]

Top 5 mad users (negative words found):
[('BondServantLZ', 24),
 ('mr_apollo', 12),
 ('fuckz', 10),
 ('swearingwatcher', 7),
 ('alexrapa', 7)]

1. Individual twitter users: 659774

2. Users with most links to other users:
[('Hollywood_Trey', 9),
 ('PamsLove', 7),
 ('tweetpet', 7),
 ('omgwtfannie', 6),
 ('loris_sl', 6),
 ('RoseStack', 5),
 ('gavlp', 5),
 ('jeremy_ellis', 5),
 ('Roonaldo107', 5),
 ('amysav83', 5)]

3. Most mentioned users
[('mileycyrus', 23),
 ('Kal_Penn', 15),
 ('stephenkruiser', 13),
 ('JonathanRKnight', 12),
 ('heidimontag', 12)]

4. Most active Twitter users:
[('lost_dog', 549),
 ('webwoke', 345),
 ('tweetpet', 310),
 ('SallytheShizzle', 281),
 ('VioletsCRUK', 279),
 ('mcraddictal', 276),
 ('tsarnick', 248),
 ('what_bugs_u', 246),
 ('Karen230683', 238),
 ('DarkPiano', 236)]
```

## Notes

The sentiment analysis is not quite sophisticated. We take a list of happy and sad words and compare to each word in the tweets. While some words carry a negative meaning, the tweets might still have a positive attitude as a whole.

I had difficulty appending the id's to the beginning of the dataset (the `sed` command did not work on my machine) hence I kept the zipped training data in the repository.