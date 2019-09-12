# FOOTBALL dataset

## Introduction

This dataset contains transcripts of 1,455 full game broadcasts from the U.S. National Football League (NFL) and National Collegiate Athletic Association (NCAA) recorded between 1960 2019.
Each row in the dataset contains the player name (first and last name), position, race, teams that played in the game the context is from, year of the player mention, and the mention context itself. For more information, see our EMNLP 2019 paper which describes the dataset: [Investigating Sports Commentator Bias within a Large Corpus of American Football Broadcasts](#)

## Contents
1455 total games (601 NFL, 854 NCAA), 27,144,587 tokens. A total of 545,232 mentions of players labeled for position and name, of which 267,778 are also tagged for race (white, nonwhite). A total of 23,313 unique football players appear in the dataset (4,604 distinct players with race labeled).

In additions to the player mention context dataset, we include the raw transcripts as obtained from YouTube, as well as team roster data split by league. All of the data is available here:
https://drive.google.com/open?id=1V_z1XWmKNXfD0CxFCwyV-nZY2otNiaZH

Each entry in our dataset has a `label` and a `mention`. The `label` stores information on the player mentioned including: name, race, reference (e.g. first name or last name only -- however the commentators referred to the player), the teams playing in the game, and the year the mention is from. The `mention` is a list of tokens containing the mention context. Player names not pertaining to the player in the `label` are replaced with the special `<player>` token.

## How mentions are obtained

We collect the mentions by taking k tokens before and after the player mention. For example if k=4 for the mention “this is a guy Jesse James does nothing but work”, the corresponding mention would be a list of tokens: [‘this’, ‘guy’, ‘does’, ‘nothing’, ‘but’, ‘work’]. Within our dataset we collect mentions with window sizes (k) of 5, 6, 8, 10, 12, 15. Note that mention context windows that contain more than one player mention are omitted.

## Processing mentions

We tokenized transcripts using spaCy. We then tag the dataset using ARK TweetNLP POS. Additionally, we use phrasemachine to identify all corpus noun phrases

## File naming convention
All files are named by the following naming convention. `football-k.json` where `k` is the number of tokens included in the mention context on either side of a name mention.

## Citation
If you use this dataset or code for your research, please cite:

    @inproceedings{football2019,
      Author = {Jack Merullo and Luke Yeh and Abram Handler and Alvin Grissom II and Brendan O'Connor and Mohit Iyyer},
      Booktitle = {Empirical Methods in Natural Language Processing},
      Year = "2019",
      Title = {Investigating Sports Commentator Bias within a Large Corpus of American Football Broadcasts.}
    }
