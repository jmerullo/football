#!/usr/bin/env bash

# get games in connl format
python games2connl.py

# run the ark tagger
find games/*connl | grep -v ark | parallel -j 5 --eta "./ark-tweet-nlp-0.3.2/runTagger.sh {} > {}.ark"

# get phrases
find games/*ark | parallel 'python arc_postproc.py -fn {} -K 5 -phrases'
