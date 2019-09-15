from collections import Counter

import socket
 
if socket.gethostname() == "dewey":
    from tqdm import  tqdm_notebook as tqdm
else:
    from tqdm import tqdm
import csv
import pandas as pd 
import numpy as np
import sys
sys.path.append("..")
sys.path.append("loglin")
import l1gen

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-fn', type=str, default=None)
args = parser.parse_args()

positions = ['OT', 'DT', 'DE', 'TE', 'LB', 'DB', 'RB', 'WR', 'QB']

MINTHRESH = 20

dt = pd.read_csv(args.fn,header=None, names=["w","e","r","p"])

positions  = set(positions)

etoks1 = [i for i in set(dt["e"]) if type(i) == str]
etoks2 = [j for i in etoks1 for j in i.split(" ")]

stops = set(etoks2) | set(etoks1)
stops = stops | set([i.replace("\n", "").replace("_", " ") for i in open("stopwords.txt")])
vocab = set(i for i in dt["w"].tolist() if i not in stops)

dt = dt[dt["w"].isin(vocab)]

# add columns for position
for p in positions:
    dt[p] = dt["p"] == p

# get rid of UNK race and filter out some positions
dt = dt[dt["r"] != "UNK"]
dt = dt[dt["p"].isin(positions)]


# filter words that only apply to 20 or fewer E 
ETHRESH = 20
gk = dt.groupby('w').agg({'e': lambda x: len(set(x))}).reset_index()
included = gk[gk["e"] > ETHRESH]["w"]
dt = dt[dt["w"].isin(included)]
        
# filter V, based on subcorpus
counts = Counter(dt["w"].tolist())
vocab = set([i for i in dt["w"].tolist() if counts[i] > MINTHRESH])
v2n = {v:k for k,v in enumerate(vocab)}
dt = dt[dt["w"].isin(vocab)]

# make e2p and e2r lookups
e = dt["e"].tolist() # these have dupes but that is OK cuz dicts dedupe below
r = dt["r"].tolist()
p = dt["p"].tolist()
e2r = {e:r for e,r in list(set(zip(e,r)))}
e2p = {e:p for e,p in list(set(zip(e,p)))}

# make position index lookups
p2n = {v:k + 1 for k,v in enumerate(positions)} # plus 1 cuz Y indexes start at race

# make e2n and v2n
E = set(dt["e"].tolist())
e2n = {v:k for k,v in enumerate(E)}


X = np.zeros((len(E), len(vocab)))
Y = np.zeros((len(E), len(positions) + 1))

for e in tqdm(E):
    # get words for each E
    e_words = Counter(dt[dt['e'] == e]["w"].tolist())
    for v in e_words:
        X[e2n[e]][v2n[v]] = e_words[v]
    Y[e2n[e]][0] = 1 if e2r[e] == "white" else 0
    Y[e2n[e]][p2n[e2p[e]]] = 1
    
gamma, beta = l1gen.train(trainX=X, trainY=Y,
                          l1_penalty=1.0)

n2v = {v:k for k,v in v2n.items()}

def top_covar(K, covar_ix, covarname, of):

    white_gamma = [(ix,v) for ix, v in enumerate(gamma[covar_ix])]

    white_gamma.sort(key=lambda x:x[1], reverse=True)

    l1 = "top {}:".format(covarname)
    l2 = ",".join([n2v[ix] for ix,v in white_gamma[0:K]])
    of.write(l1 + "\n")
    of.write(l2 + "\n")
    print(l1)
    print(l2)

    
    
with open("report.txt", "w") as of:
    top_covar(20, 0, "white", of)
    for position in positions:
        top_covar(20, p2n[position], position, of)
