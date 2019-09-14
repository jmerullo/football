import json, argparse
from collections import Counter, defaultdict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='name analysis')
    parser.add_argument('--data', type=str, default='../dataset/FOOTBALL/football_12.json',
            help='processed FOOTBALL json location')
    parser.add_argument('--position', type=str, default='QB',
            help='what position to do the analysis on\
                  (e.g., QB, RB, WR, TE, DB, etc.')
    args = parser.parse_args()

    data = json.load(open(args.data, 'rb'))
    print('number of total mentions: %d' % len(data))
    print('analyzing %s mentions\n' % args.position)

    race_refs = {'white':Counter(), 'nonwhite':Counter()}
    pos_refs = defaultdict(Counter)

    for key in data.keys():
        ex = data[key]
        name = ex['label']['player']
        ref = ex['label']['reference']
        race = ex['label']['race']
        pos = ex['label']['position']

        if pos != args.position:
            continue

        split = name.split()

        # ignore names that don't have exactly two parts for simplicity
        if len(split) == 2:

            if ref == split[0]:
                race_refs[race]['first name'] += 1
                pos_refs[pos]['first name'] += 1

            elif ref == split[1]:
                race_refs[race]['last name'] += 1
                pos_refs[pos]['last name'] += 1

            elif ref == name:
                race_refs[race]['full name'] += 1
                pos_refs[pos]['full name'] += 1

    # display stats by race
    for key in race_refs:
        print('name references for %s %s:' % (key, args.position))
        c = race_refs[key]
        norm = float(sum(c.values()))
        for reftype in sorted(c):
            print('%s: %d out of %d, %0.2f%%' % (reftype, c[reftype], norm, c[reftype] * 100. / norm))
        print()

    # display overall stats
    for key in pos_refs:
        print('name references for all %s:' % args.position)
        c = pos_refs[key]
        norm = float(sum(c.values()))
        for reftype in sorted(c):
            print('%s: %d out of %d, %0.2f%%' % (reftype, c[reftype], norm, c[reftype] * 100. / norm))
        print()
