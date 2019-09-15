
# this lexicon was constructed by first taking the intersection of publically-
# available subreddit-specific lexicons from r/NFL, r/CFB, and r/sports
# (https://nlp.stanford.edu/projects/socialsent/). Next, we pared down the
# lexicon by manually removing reddit-specific slang. Finally, we added words
# that had been used in prior social science papers studying sentiment
# patterns in sports commentator bias. As all such papers relied on manual
# coding, we obtained these words by looking at coded examples in the paper
# text and tables. This lexicon is by no means complete, and we hope that
# future work can expand on our approach by either augmenting the lexicon or
# using more powerful sentiment analysis techniques.


neg = ['aggressive', 'anger', 'annoying', 'arrogant', 'asshole', 'assholes',
'awful', 'bad', 'bandwagon', 'bias', 'bitching', 'bite', 'bitter', 'blame',
'blaming', 'blatant', 'blind', 'bs', 'bullshit', 'choke', 'choking', 'clown',
'cocky', 'complain', 'crap', 'crappy', 'critical', 'damage', 'defeat',
'destroy', 'die', 'dirty', 'disgusting', 'dislike', 'douche', 'drama',
'dubious', 'dumb', 'dumbass', 'dumbest', 'easiest', 'ejected', 'embarrassing',
'entitled', 'exception', 'excuse', 'excuses', 'fault', 'fool', 'foolish',
'frustrating', 'garbage', 'gross', 'haters', 'hating', 'hatred', 'helpless',
'horrible', 'idiot', 'idiotic', 'idiots', 'ignorant', 'illegal',
'intentional', 'jerk', 'judgement', 'mediocre', 'mess', 'mistakes', 'moron',
'nightmare', 'non', 'nonsense', 'obnoxious', 'pain', 'painful', 'pathetic',
'personality',  'piss', 'planet', 'poor', 'questionable', 'rage', 'regret',
'responsible', 'retarded', 'rival', 'rivalries', 'rivalry', 'rivals', 'rude',
'ruined', 'screw', 'severe', 'shame', 'shitting', 'shitty', 'shocking',
'soft', 'stink', 'stinking', 'stunk', 'struggle', 'struggling', 'stupid',
'suck', 'sucked', 'sucking', 'sucks', 'suffer', 'suffered', 'surprising',
'suspect', 'terrible', 'trash', 'unfortunate', 'unintelligent', 'unnecessary',
'untalented', 'unwise', 'virtually', 'weak', 'whining', 'worse', 'worthless']


pos = ['ability', 'absurd', 'all-time', 'animal', 'appreciate', 'athletic',
'athleticism', 'awareness', 'awesome', 'badass', 'beast', 'beautiful',
'beauty', 'bold', 'brilliant', 'bull', 'caliber', 'calm', 'christ', 'class',
'classic', 'classy', 'congratulations', 'cool', 'crazy', 'damn', 'damnit',
'dear', 'diligent', 'easy', 'elite', 'enjoy', 'enjoyed', 'enjoying',
'entertaining', 'entertainment', 'epic', 'excellent', 'excited', 'familiar',
'fantastic', 'favorite', 'flamboyant', 'flash', 'freak', 'freaking',
'friendly', 'fuckin', 'fucking', 'fun', 'funny', 'generational', 'gift',
'gifted', 'glad', 'glorious', 'glory', 'goddamn', 'good', 'grade', 'great',
'hardworking', 'highest', 'hilarious', 'holy', 'honest', 'humble',
'impressed', 'impressive', 'inappropriate', 'incredible', 'inhuman', 'insane',
'interested', 'interesting', 'jesus', 'kidding', 'liked',
'literally','logical', 'lord', 'love', 'loving', 'ludicrous', 'miracle',
'monster', 'nailed', 'natural', 'nickname', 'nuts', 'outstanding', 'perfect',
'phenomenal', 'playmaker', 'prime','quiet', 'recommend', 'reflexes',
'ridiculous', 'safe', 'savior', 'simple', 'smart', 'special', 'spectacular',
'speed', 'strong', 'stronger', 'superstar', 'talent', 'talented',
'unbelievable', 'unique', 'unreal', 'versatile', 'whoa', 'wish', 'wise',
'woah', 'wonderful', 'wow', ]
