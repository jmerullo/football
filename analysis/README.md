# FOOTBALL sentiment / name analysis scripts

## requirements
Running this code requires Python 3, no other dependencies needed!

## commands to replicate the paper's analysis

First, make sure you've downloaded the dataset and unzipped it in the parent directory. Then, to replicate the name reference analysis in Table 3 of the paper, run the following commands:

```
python reference_analysis.py --position QB
python reference_analysis.py --position WR
python reference_analysis.py --position RB
python reference_analysis.py --position TE
```

You can also experiment with other positions if you'd like! The full list of positions is 'QB', 'DB', 'RB', 'WR', 'C', 'DE', 'LB', 'DT', 'TE', 'OT', 'OG', 'DL', 'OL', 'LS'. Please note that the number of mentions for some positions is sparse, as they are less likely to be singled out by commentators. 

To replicate the sentiment analysis results in Table 4, run the following:

```
python sentiment_analysis.py --position ALL 
python sentiment_analysis.py --position QB
```

Some options you may want to play around with are "single_player", which removes windows that contain mentions to two or more different players from consideration, and "occ_thresh", which controls how many times a word in the lexicon must occur for both races to be considered. 
