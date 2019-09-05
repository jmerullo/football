# NFL/NCAA Broadcast Dataset

## Introduction

This dataset contains transcripts of 1,455 full game broadcasts from the U.S. National Football League (NFL) and National Collegiate Athletic Association (NCAA) recorded between 1960 2019.
Each row in the dataset contains the player name (first and last name), position, race, teams that the player has played on, year of the player mention, and the mention itself.

## Contents
1455 total games (601 NFL, 854 NCAA), 27,144,587 tokens. A total of 545,232 mentions of players labeled for position and name, of which 267,778 are also tagged for race (white, nonwhite). A total of 23,313 unique football players appear in the dataset (4,604 distinct players with race labeled).

In additions to the player mention context dataset, we include the raw transcripts as obtained from YouTube, as well as team roster data split by league.

## How mentions are obtained

We collect the mentions by taking k tokens before and after the player mention. For example if k=4 for the mention “this is a guy Jesse James does nothing but work”, the corresponding mention would be a list of tokens: [‘this’, ‘guy’, ‘does’, ‘nothing’, ‘but’, ‘work’]. Within our dataset we collect mentions with window sizes (k) of 5, 6, 8, 10, 15.

## Processing mentions

We tokenized transcripts using spaCy. We then tag the dataset using ARK TweetNLP POS. Additionally, we use phrasemachine to identify all corpus noun phrases

## File naming convention
All files are named by the following naming convention. `sports-bias-k.pkl` where `k` is the number of tokens included in the mention context on either side of a name mention.

## More information
For more information see our paper: [link to paper]
