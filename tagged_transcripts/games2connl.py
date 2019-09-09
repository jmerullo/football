# one script that gets all games innto connly format
import json
import re
from tqdm import tqdm

PERSON_START_TAG = "<person[^>]+>"
PERSON_END_TAG = "</person>"
FAKE_SPACE = "&&&&"
ANYTAG = PERSON_START_TAG + "|" + PERSON_END_TAG

toks_metadata = []
toks = []


def do_connl(fn): 

    with open(fn, 'r') as inf:
        dt = json.load(inf)
     
    of = fn.replace(".json", ".connl")

    v = dt

    transcript = v['transcript']
    transcript = transcript.replace("</person>", " </person>").replace('">', '"> ')
    for i in re.findall(PERSON_START_TAG, transcript):
        transcript = transcript.replace(i, i.replace(" ", "&&&&"))
    counter = 0
    person_mode = False
    metadata = "NONE"
    for t in transcript.split(" "):
        add_token = True 
        if "<perso" in t:
            person_mode = True
            metadata = t
            add_token = False
        if "</perso" in t:
            person_mode = False
            metadata = "NONE"
            add_token = False
        if add_token:
            toks.append(t)
            toks_metadata.append(metadata)

    counter = 0

    with open(of, "w") as of:
        for t, md in zip(toks, toks_metadata):
            of.write("\t".join([t,md]) + "\n")
            counter += 1
            if counter % 200 == 0:
                of.write("\n")


if __name__ == '__main__':
    tagged ='tagged_transcripts.json'
    for fn in [tagged]:
        with open(fn, "r") as inf:
            games = json.load(inf)
        for game_name, game in tqdm(games.items()): 
            game["sourcefn"] = fn
            with open("games/" + game_name  + ".json", "w") as of:
                of.write(json.dumps(game) + '\n')
            do_connl("games/" + game_name + ".json")
