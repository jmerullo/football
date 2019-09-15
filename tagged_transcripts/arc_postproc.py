#import ipdb;ipdb.set_trace() takes an .ark output file and builds mentions as jsonl 
# to run largescale run $find *ark | parallel -j 20 --eta "python abe_postproc.py -fn {} -K 5"


from tqdm import tqdm as tqdm
from copy import deepcopy

from subprocess import check_output
import re
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-fn', type=str, default=None)
parser.add_argument("-phrases", dest="phrases", action='store_true')
parser.add_argument('-K', type=int, default=None)
#parser.add_argument('-VP', dest="VP", action='store_true')
parser.add_argument('-filter_to_just_a', dest='filter_to_just_a', action='store_true')
args = parser.parse_args()

fn = args.fn

assert args.fn is not None
assert args.K is not None
print(args)
all_mentions = []

grepargs = ['grep', 'person', fn, "-B", str(args.K), "-A", str(args.K)]

# this should block
out = str(check_output(grepargs)).split("\\n")

l = []
for i in tqdm(out):
    l.append(i.split("\\t"))
    if '--' in i:
        mention = {"words": [], "metadata": None}
        for item in l:
            if item[0] != "--" and item[0] != "": 
                word, tag, metadata = item[0], item[1], item[4] 
                if "&&&" in metadata: 
                    race, position = metadata.split("&&&")[-2:]
                    race = race.replace('&race=', '').replace('/', '').replace('\\\\', '')
                    position = position.replace("&position=", "").replace('/','').replace("\\\\","").replace(">", "")
                    person = [i for i in metadata.split("&&&") if "person" not in i and "position" not in i and "race" not in i] 
                    person = [i.replace('"', '').replace("player","").replace("&", "").replace("=","") for i in person]
                    race = race.replace('"', '')
                    position = position.replace('"', '') 
                    mention["metadata"] = {"race": race, "position": position, 'player': person}
                mention['words'].append({'word': word, 'tag': tag})
        if mention['metadata'] is not None: # a few false posotives for the word "person" from grerp
            all_mentions.append(mention)
        l = []


if args.filter_to_just_a:
    filter_a = args.filter_to_just_a

    with open(fn + ".{}.mentions.filtera={}.csv".format(args.K, str(filter_a)), "w") as of:
        for l in all_mentions:
            player = " ".join(l["metadata"]["player"])
            race = l["metadata"]["race"]
            position = l["metadata"]["position"]
            for w in l["words"]:
                if w["tag"] == "A":
                    of.write(','.join([w["word"], player, race, position]) + "\n")

if args.phrases:
    from phrasemachine import get_phrases
    with open(fn + ".{}.mentions.phrases.csv".format(args.K), "w") as of:
        for l in all_mentions:
            player = " ".join(l["metadata"]["player"])
            race = l["metadata"]["race"]
            position = l["metadata"]["position"]
            toks = [i["word"] for i in l["words"]]
            pos = [i["tag"] for i in l["words"]]
            assert len(toks) == len(pos)
            try:
                phrases = get_phrases(tokens=toks, postags=pos)
            except IndexError:
                phrases = {"counts":{}}
            phrases = [o for o in phrases["counts"].keys()]
            As = [i["word"] for i in l['words'] if i['tag'] == 'A']
            phrasetoks = [i for p in phrases for i in p.split(" ")]
            for w in phrases:
                of.write(",".join([w,player,race,position]) + '\n')
            for a in As:
                if a not in phrasetoks:
                    of.write(",".join([a,player,race,position]) + '\n')


'''

def get_mentions(K, fn):

    grepargs = ['grep', 'person', fn, "-B", str(K), "-A", str(K)]

    # this should block
    out = str(check_output(grepargs)).split("\\n")

    out = [i for i in str(check_output(grepargs)).split("\\n")]
    
    all_mentions = []
    l = []
    for i in tqdm(out):
        l.append(i.split("\\t"))
        if '--' in i:
            mention = {"words": [], "metadata": None}
            for item in l:
                if item[0] != "--" and item[0] != "":
                    word, tag, metadata = item[0], item[1], item[4]
                    if "&&&" in metadata:
                        race, position = metadata.split("&&&")[-2:]
                        race = race.replace('&race=', '').replace('/', '').replace('\\\\', '')
                        position = position.replace("&position=", "").replace('/','').replace("\\\\","").replace(">", "")
                        person = [i for i in metadata.split("&&&") if "person" not in i and "position" not in i and "race" not in i]
                        person = [i.replace('"', '').replace("player","").replace("&", "").replace("=","") for i in person]
                        race = race.replace('"', '')
                        position = position.replace('"', '')
                        mention["metadata"] = {"race": race, "position": position, 'player': person}
                    mention['words'].append({'word': word, 'tag': tag})
            if mention['metadata'] is not None: # a few false posotives for the word "person" from grerp
                all_mentions.append(mention)
            l = []
    return all_mentions      


def limited_A(mentions, of):

    regex = "\^VD?AN?"

    of.write("w,e,r,p\n")
    VPs = []
    for l in mentions:
        player = " ".join(l["metadata"]["player"])
        race = l["metadata"]["race"]
        position = l["metadata"]["position"]
        words = [i["word"] for i in l["words"]]
        tags = [i["tag"] for i in l["words"]]
        str_ = "".join(tags)
        for r in re.finditer(regex, str_):
            s,e = r.span()
            if 'is' in words:
                w = " ".join(words[s + 1: e]).replace(",", "")
                of.write(",".join([w,player,race,position]) + '\n')


if args.VP:
    with open(args.fn + ".vp", "w") as of: 
        mentions = get_mentions(K=args.K, fn = args.fn)
        limited_A(mentions, of)
'''
