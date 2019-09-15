import json, argparse
from collections import Counter, defaultdict
from filtered_lexicons import neg,pos

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='sentiment analysis')
    parser.add_argument('--data', type=str, default='../dataset/FOOTBALL/football_12.json',
            help='processed FOOTBALL json location')
    parser.add_argument('--position', type=str, default='QB',
            help="FYI positions other than QB lack enough data,\
                  if ALL, looks at all positions")
    parser.add_argument('--single_player', type=bool, default=0,
            help="filter out windows that contain \
                  mentions of multiple players")
    parser.add_argument('--occ_thresh', type=int, default=10,
            help="a sentiment word must occur at least this many\
                  times in BOTH nonwhite and white windows to be\
                  considered for this analysis")
    args = parser.parse_args()
    data = json.load(open(args.data, 'rb'))

    # some counters to store info
    overall = Counter()
    position = defaultdict(Counter)
    total_ment = Counter()
    race = defaultdict(Counter)
    pos_word_count = defaultdict(Counter)
    neg_word_count = defaultdict(Counter)

    # sentiment lexicons
    pset = set(pos)
    nset = set(neg)
    print('The lexicon contains %d positive and %d negative words'\
        % (len(pos), len(neg)))


    # initial pass through the data
    # identify positive/negative windows
    for key in data:
        strment = ' '.join(data[key]['mention']) # text
        r = data[key]['label']['race'] # race
        p = data[key]['label']['position'] # position

        # option: only consider players with a certain position
        if args.position != 'ALL' and p != args.position:
            continue

        # option: remove windows w/ multiple player mentions
        if args.single_player and ('<' in strment or '>' in strment):
            continue

        total_ment[p] += 1.
        total_ment[r] += 1.
        neg_count = 0.
        pos_count = 0.
        for w in data[key]['mention']:
            if w in pos:
                pos_count += 1
                pos_word_count[p][w] += 1 # count word by position
                pos_word_count[r][w] += 1 # count word by race
                # print ('POS: ', w, '||||', strment)

            elif w in neg:
                neg_count += 1
                neg_word_count[p][w] += 1
                neg_word_count[r][w] += 1
                # print ('NEG: ', w, '||||', strment)

        # handle multiple polarity sentiment matches in a single window
        # by assigning the window to the majority polarity
        if neg_count > 0 and neg_count > pos_count:
            overall['neg'] += 1
            race[r]['neg'] += 1
            position[p]['neg'] += 1
        if pos_count > 0 and pos_count > neg_count:
            overall['pos'] += 1
            race[r]['pos'] += 1
            position[p]['pos'] += 1


    # let's now print out some summary stats per position
    # showing raw counts of neg/pos mentions
    # sanity check: % of negative mentions is relatively low
    # across all positions and similar to numbers reported in prev work
    print('SUMMARY ACROSS ALL POSITIONS')
    total_pos = 0.
    total_neg = 0.
    total_mentions = 0.
    for key in position:
        print('%s: %d negative, %d positive, %0.2f%% negative, %d total mentions, %0.2f%% polar' \
            % (key, position[key]['neg'], position[key]['pos'], 
                position[key]['neg']*100 / sum(position[key].values()), total_ment[key],
                sum(position[key].values()) * 100 / total_ment[key]))
        print('positive words', pos_word_count[key].most_common(15))
        print('negative words', neg_word_count[key].most_common(15))
        print ('')
        total_pos += position[key]['pos']
        total_neg += position[key]['neg']
        total_mentions += total_ment[key]

    print('%s: %d negative, %d positive, %0.2f%% negative, %d total mentions, %0.2f%% polar\n' \
            % ('total', total_neg, total_pos, 100.0* total_neg / (total_neg + total_pos), total_mentions, 100.0 * (total_pos + total_neg) / total_mentions)) 
    print('\n\n============================\n\n')


    # summary stats by race
    print('SUMMARY ACROSS RACE')
    for key in race:
        print('%s: %d negative, %d positive, %0.2f%% negative, %d total mentions, %0.2f%% polar' \
            % (key, race[key]['neg'], race[key]['pos'], 
                race[key]['neg']*100 / sum(race[key].values()), total_ment[key],
                sum(race[key].values()) * 100 / total_ment[key]))

        print ('positive words')
        for w, v in pos_word_count[key].most_common(25):
            print ('%s: %d out of %d, %0.2f%%' % (w, v,
                sum(pos_word_count[key].values()), 100.* v/sum(pos_word_count[key].values())  ))
        print ('')
        print ('negative words')
        for w, v in neg_word_count[key].most_common(25):
            print ('%s: %d out of %d, %0.2f%%' % (w, v,
                sum(neg_word_count[key].values()), 100.* v/sum(neg_word_count[key].values())  ))
        print ('')
    print('\n============================\n\n')


    # now let's dig a little further by computing % of sent. words used by race, 
    # so we can see if particular words are used more frequently
    # to positively or negatively describe white vs nonwhite players
    neg_percs = defaultdict(dict)
    pos_percs = defaultdict(dict)
    for key in race:
        for w in neg_word_count[key]:

            # a word must occur enough across both races, otherwise 
            # comparing its usage frequency is prob. misleading / uninformative
            if neg_word_count['white'][w] > args.occ_thresh and neg_word_count['nonwhite'][w] > args.occ_thresh:
                neg_percs[w][key] = 100.* neg_word_count[key][w]/sum(neg_word_count[key].values())
       
        for w in pos_word_count[key]:
            if pos_word_count['white'][w] > args.occ_thresh and pos_word_count['nonwhite'][w] > args.occ_thresh:
                pos_percs[w][key] = 100.* pos_word_count[key][w]/sum(pos_word_count[key].values())


    # now let's look at the ratios of these usage frequencies
    neg_diffs = Counter()
    pos_diffs = Counter()
    for w in neg_percs:
        neg_diffs[w] = neg_percs[w]['white']/neg_percs[w]['nonwhite']

    for w in pos_percs:
        pos_diffs[w] = pos_percs[w]['white']/pos_percs[w]['nonwhite']


    # now print most white/nonwhite positive/negative words!
    print('most white positive words, ranked by frequency ratio')
    for w in sorted(pos_diffs, key=lambda dict_key: -abs(pos_diffs[dict_key]))[:20]:
        try:
            print('%s, white: %0.2f%%, nonwhite: %0.2f%%, %%diff: %0.2f x' %\
                (w, pos_percs[w]['white'], pos_percs[w]['nonwhite'], pos_diffs[w]))
        except:
            pass

    print('\nmost nonwhite positive words, ranked by frequency ratio')
    for w in sorted(pos_diffs, key=lambda dict_key: abs(pos_diffs[dict_key]))[:20]:
        try:
            print('%s, white: %0.2f%%, nonwhite: %0.2f%%, %%diff: %0.2f x' %\
                (w, pos_percs[w]['white'], pos_percs[w]['nonwhite'], 1/pos_diffs[w]))
        except:
            pass

    print('\nmost white negative words, ranked by frequency ratio')
    for w in sorted(neg_diffs, key=lambda dict_key: -abs(neg_diffs[dict_key]))[:20]:
        try:
            print('%s, white: %0.2f%%, nonwhite: %0.2f%%, %%diff: %0.2f x' %\
                (w, neg_percs[w]['white'], neg_percs[w]['nonwhite'], neg_diffs[w]))
        except:
            pass

    print('\nmost nonwhite negative words, ranked by frequency ratio')
    for w in sorted(neg_diffs, key=lambda dict_key: abs(neg_diffs[dict_key]))[:20]:
        try:
            print('%s, white: %0.2f%%, nonwhite: %0.2f%%, %%diff: %0.2f x' %\
                (w, neg_percs[w]['white'], neg_percs[w]['nonwhite'], 1/neg_diffs[w]))
        except:
            pass






