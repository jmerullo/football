#!/usr/bin/env bash

# run this in a python3 venv. Once you load the venv, do $pip install -r requirements.txt to load dependencies

# get games in connl format
python games2connl.py

# run the ark tagger
find games/*connl | grep -v ark | parallel -j 5 --eta "./ark-tweet-nlp-0.3.2/runTagger.sh {} > {}.ark"

# get phrases
find games/*ark | parallel 'python arc_postproc.py -fn {} -K 5 -phrases'

# downsample
ls games/*phrases*  | xargs cat | shuf | head -1000000 > sample.csv

# run model
python ll_model.py -fn sample.csv
