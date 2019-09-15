# FOOTBALL dataset

## Introduction

This repository contains scripts to analyze and process the FOOTBALL dataset, which is built from transcripts of 1,455 full game broadcasts from the U.S. National Football League (NFL) and National Collegiate Athletic Association (NCAA) recorded between 1960 and 2019. To start, please download the dataset at the following link and extract the zip file into this directory:
https://drive.google.com/file/d/15XVD0kumvPhJkwj20an2kwWCdL9w_cy7/view?usp=sharing 

The dataset and associated experiments are described fully in our associated EMNLP 2019 paper, [Investigating Sports Commentator Bias within a Large Corpus of American Football Broadcasts](https://arxiv.org/abs/1909.03343).

## Dataset contents
FOOTBALL contains 1455 total games (601 NFL, 854 NCAA) whose transcripts amount to 27,144,587 tokens in total (tokenized with spaCy). Within these transcripts, we identify 545,232 mentions of players labeled with their position and name, of which 267,778 are also tagged for race (white, nonwhite). A total of 23,313 unique football players appear in the dataset (4,604 who we were able to label with race information). In additions to the player mention context dataset, we include the raw transcripts obtained from YouTube, as well as team roster data split by league. 

Each entry in our player mention dataset has a `label` and a `mention`. The `label` stores information about the player mentioned, including canonical name, race, reference name (i.e., how the commentators referred to the player), the teams playing in the game, and the year the mention is from. The `mention` contains tokens from a *k*-length window around the reference; for example, given the following text "this is a guy Jesse James does nothing but work", the corresponding window with *k*=4 would be: ['this', 'is', 'a', guy', 'does', 'nothing', 'but', 'work']. We provide files with multiple window sizes for convenience as `football-k.json`. If players other than the one in the label field appear in the window, any references to them are replaced with a special `<player>` token.

## Code contents
Please see the `analysis` subdirectory for scripts and instructions on how to replicate our experiments.

## Citation
If you use this dataset or code for your research, please cite:

    @inproceedings{football2019,
      Author = {Jack Merullo and Luke Yeh and Abram Handler and Alvin {Grissom II} and Brendan O'Connor and Mohit Iyyer},
      Booktitle = {Empirical Methods in Natural Language Processing},
      Year = "2019",
      Title = {Investigating Sports Commentator Bias within a Large Corpus of American Football Broadcasts.}
    }
