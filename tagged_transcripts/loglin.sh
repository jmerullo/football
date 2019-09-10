#!/usr/bin/env bash

python games2connl.py

find games/*connl | grep -v ark | parallel -j 5 --eta "./ark-tweet-nlp-0.3.2/runTagger.sh {} > {}.ark"
