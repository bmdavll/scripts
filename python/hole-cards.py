#!/usr/bin/env python3

# Texas Hold'em starting hand analysis:
#   Chen formula score
#   Sklansky group
#   Nelson category
#   expected value

import sys
import re
import math

chen = {
    'A':10,
    'K':8,
    'Q':7,
    'J':6,
    'T':5,
    '9':4.5,
    '8':4,
    '7':3.5,
    '6':3,
    '5':2.5,
    '4':2,
    '3':1.5,
    '2':1,
}

def rank(card):
    try:
        return int(card)
    except ValueError:
        return {
            'A':14,
            'K':13,
            'Q':12,
            'J':11,
            'T':10,
        } [card]

cards = ''.join(reversed(sorted(chen.keys(), key=rank)))

def gap(hand):
    return rank(hand[0]) - rank(hand[1]) - 1

def groupEquivalent(score):
    if 10 <= score <= 20:
        return 2 - (score-10)/10
    elif score == 9:
        return 3
    elif score == 8:
        return 4
    elif score == 7:
        return 5
    elif score == 6:
        return 6
    elif score == 5:
        return 7
    elif score == 4:
        return 8
    elif score < 4:
        return 9

sklansky = {
    'AA'  : 1,
    'AKs' : 1,
    'KK'  : 1,
    'QQ'  : 1,
    'JJ'  : 1,
    'AK'  : 2,
    'AQs' : 2,
    'AJs' : 2,
    'KQs' : 2,
    'TT'  : 2,
    'AQ'  : 3,
    'ATs' : 3,
    'KJs' : 3,
    'QJs' : 3,
    'JTs' : 3,
    '99'  : 3,
    'AJ'  : 4,
    'KQ'  : 4,
    'KTs' : 4,
    'QTs' : 4,
    'J9s' : 4,
    'T9s' : 4,
    '98s' : 4,
    '88'  : 4,
    'A9s' : 5,
    'A8s' : 5,
    'A7s' : 5,
    'A6s' : 5,
    'A5s' : 5,
    'A4s' : 5,
    'A3s' : 5,
    'A2s' : 5,
    'KJ'  : 5,
    'QJ'  : 5,
    'Q9s' : 5,
    'JT'  : 5,
    'T8s' : 5,
    '97s' : 5,
    '87s' : 5,
    '77'  : 5,
    '76s' : 5,
    '66'  : 5,
    'AT'  : 6,
    'KT'  : 6,
    'QT'  : 6,
    'J8s' : 6,
    '86s' : 6,
    '75s' : 6,
    '65s' : 6,
    '55'  : 6,
    '54s' : 6,
    'K9s' : 7,
    'K8s' : 7,
    'K7s' : 7,
    'K6s' : 7,
    'K5s' : 7,
    'K4s' : 7,
    'K3s' : 7,
    'K2s' : 7,
    'Q8s' : 7,
    'J9'  : 7,
    'T9'  : 7,
    'T7s' : 7,
    '98'  : 7,
    '64s' : 7,
    '53s' : 7,
    '44'  : 7,
    '43s' : 7,
    '33'  : 7,
    '22'  : 7,
    'A9'  : 8,
    'K9'  : 8,
    'Q9'  : 8,
    'J8'  : 8,
    'J7s' : 8,
    'T8'  : 8,
    '96s' : 8,
    '87'  : 8,
    '85s' : 8,
    '76'  : 8,
    '74s' : 8,
    '65'  : 8,
    '54'  : 8,
    '42s' : 8,
    '32s' : 8,
}

nelson = {
    'AA'  : 1,
    'KK'  : 1,
    'AKs' : 2,
    'AK'  : 2,
    'QQ'  : 2,
    'JJ'  : 2,
    'AQs' : 3,
    'AQ'  : 3,
    'TT'  : 3,
    '99'  : 3,
    'AJs' : 4,
    'KQs' : 4,
    '88'  : 4,
    '77'  : 4,
    'AJ'  : 5,
    'ATs' : 5,
    'AT'  : 5,
    'KQ'  : 5,
    'KJs' : 5,
    '66'  : 5,
    '55'  : 5,
    'A9s' : 6,
    'A8s' : 6,
    'A7s' : 6,
    'A6s' : 6,
    'A5s' : 6,
    'A4s' : 6,
    'A3s' : 6,
    'A2s' : 6,
    'KJ'  : 6,
    'KTs' : 6,
    'QJs' : 6,
    'QTs' : 6,
    'JTs' : 6,
    '44'  : 6,
    '33'  : 6,
    '22'  : 6,
    'A9'  : 7,
    'A8'  : 7,
    'A7'  : 7,
    'A6'  : 7,
    'A5'  : 7,
    'A4'  : 7,
    'A3'  : 7,
    'A2'  : 7,
    'KT'  : 7,
    'QJ'  : 7,
    'QT'  : 7,
    'JT'  : 7,
    'T9s' : 7,
    '98s' : 7,
    '87s' : 7,
    '76s' : 7,
    '65s' : 7,
    '54s' : 7,
    'K9s' : 8,
    'K9'  : 8,
    'K8s' : 8,
    'Q9s' : 8,
    'Q8s' : 8,
    'J9s' : 8,
    'T9'  : 8,
    'T8s' : 8,
    '98'  : 8,
    '97s' : 8,
    '87'  : 8,
    '86s' : 8,
    '76'  : 8,
    '75s' : 8,
    '64s' : 8,
}

ftr = {
    'AA'  : 1,
    'KK'  : 1,
    'AKs' : 2,
    'QQ'  : 2,
    'JJ'  : 2,
    'AK'  : 3,
    'AQs' : 3,
    'AJs' : 3,
    'KQs' : 3,
    'TT'  : 3,
    'AQ'  : 4,
    'ATs' : 4,
    'KJs' : 4,
    '99'  : 4,
    '88'  : 4,
    '77'  : 4,
    'AJ'  : 5,
    'AT'  : 5,
    'KQ'  : 5,
    'KTs' : 5,
    'QJs' : 5,
    'JTs' : 5,
    'A9s' : 6,
    'A8s' : 6,
    'KJ'  : 6,
    'QJ'  : 6,
    'QTs' : 6,
    '66'  : 6,
    '55'  : 6,
    '44'  : 6,
    '33'  : 6,
    '22'  : 6,
    'A7s' : 7,
    'A6s' : 7,
    'A5s' : 7,
    'A4s' : 7,
    'A3s' : 7,
    'A2s' : 7,
    'KT'  : 7,
    'K9s' : 7,
    'QT'  : 7,
    'Q9s' : 7,
    'JT'  : 7,
    'J9s' : 7,
    'T9s' : 7,
    'A9'  : 8,
    'K9'  : 8,
    '98s' : 8,
    '87s' : 8,
}

ev = {
    'AA'  : 2.32,
    'KK'  : 1.67,
    'QQ'  : 1.22,
    'JJ'  : 0.86,
    'AKs' : 0.78,
    'AQs' : 0.59,
    'TT'  : 0.58,
    'AK'  : 0.51,
    'AJs' : 0.44,
    'KQs' : 0.39,
    '99'  : 0.38,
    'ATs' : 0.32,
    'AQ'  : 0.31,
    'KJs' : 0.29,
    '88'  : 0.25,
    'QJs' : 0.23,
    'KTs' : 0.20,
    'A9s' : 0.19,
    'AJ'  : 0.19,
    'QTs' : 0.17,
    'KQ'  : 0.16,
    '77'  : 0.16,
    'JTs' : 0.15,
    'A8s' : 0.10,
    'K9s' : 0.09,
    'AT'  : 0.08,
    'A5s' : 0.08,
    'A7s' : 0.08,
    'KJ'  : 0.08,
    '66'  : 0.07,
    'T9s' : 0.05,
    'A4s' : 0.05,
    'Q9s' : 0.05,
    'J9s' : 0.04,
    'QJ'  : 0.03,
    'A6s' : 0.03,
    '55'  : 0.02,
    'A3s' : 0.02,
    'K8s' : 0.01,
    'KT'  : 0.01,
    '98s' : 0.00,
    'A2s' : 0.00,
    'T8s' : -0.00,
    'K7s' : -0.00,
    '87s' : -0.02,
    'QT'  : -0.02,
    'Q8s' : -0.02,
    '44'  : -0.03,
    'A9'  : -0.03,
    'J8s' : -0.03,
    '76s' : -0.03,
    'JT'  : -0.03,
    '97s' : -0.04,
    'K6s' : -0.04,
    'K5s' : -0.05,
    'K4s' : -0.05,
    'T7s' : -0.05,
    'Q7s' : -0.06,
    'K9'  : -0.07,
    '65s' : -0.07,
    'T9'  : -0.07,
    '86s' : -0.07,
    'A8'  : -0.07,
    'J7s' : -0.07,
    '33'  : -0.07,
    '54s' : -0.08,
    'Q6s' : -0.08,
    'K3s' : -0.08,
    'Q9'  : -0.08,
    '75s' : -0.09,
    '22'  : -0.09,
    'J9'  : -0.09,
    '64s' : -0.09,
    'Q5s' : -0.09,
    'K2s' : -0.09,
    '96s' : -0.09,
    'Q3s' : -0.10,
    'J8'  : -0.10,
    '98'  : -0.10,
    'T8'  : -0.10,
    '97'  : -0.10,
    'A7'  : -0.10,
    'T7'  : -0.10,
    'Q4s' : -0.10,
    'Q8'  : -0.11,
    'J5s' : -0.11,
    'T6'  : -0.11,
    '75'  : -0.11,
    'J4s' : -0.11,
    '74s' : -0.11,
    'K8'  : -0.11,
    '86'  : -0.11,
    '53s' : -0.11,
    'K7'  : -0.11,
    '63s' : -0.11,
    'J6s' : -0.11,
    '85'  : -0.11,
    'T6s' : -0.11,
    '76'  : -0.11,
    'A6'  : -0.12,
    'T2'  : -0.12,
    '95s' : -0.12,
    '84'  : -0.12,
    '62'  : -0.12,
    'T5s' : -0.12,
    '95'  : -0.12,
    'A5'  : -0.12,
    'Q7'  : -0.12,
    'T5'  : -0.12,
    '87'  : -0.12,
    '83'  : -0.12,
    '65'  : -0.12,
    'Q2s' : -0.12,
    '94'  : -0.12,
    '74'  : -0.12,
    '54'  : -0.12,
    'A4'  : -0.12,
    'T4'  : -0.12,
    '82'  : -0.12,
    '64'  : -0.12,
    '42'  : -0.12,
    'J7'  : -0.12,
    '93'  : -0.12,
    '85s' : -0.12,
    '73'  : -0.12,
    '53'  : -0.12,
    'T3'  : -0.12,
    '63'  : -0.12,
    'K6'  : -0.12,
    'J6'  : -0.12,
    '96'  : -0.12,
    '92'  : -0.12,
    '72'  : -0.12,
    '52'  : -0.12,
    'Q4'  : -0.13,
    'K5'  : -0.13,
    'J5'  : -0.13,
    '43s' : -0.13,
    'Q3'  : -0.13,
    '43'  : -0.13,
    'K4'  : -0.13,
    'J4'  : -0.13,
    'T4s' : -0.13,
    'Q6'  : -0.13,
    'Q2'  : -0.13,
    'J3s' : -0.13,
    'J3'  : -0.13,
    'T3s' : -0.13,
    'A3'  : -0.13,
    'Q5'  : -0.13,
    'J2'  : -0.13,
    '84s' : -0.13,
    '82s' : -0.14,
    '42s' : -0.14,
    '93s' : -0.14,
    '73s' : -0.14,
    'K3'  : -0.14,
    'J2s' : -0.14,
    '92s' : -0.14,
    '52s' : -0.14,
    'K2'  : -0.14,
    'T2s' : -0.14,
    '62s' : -0.14,
    '32'  : -0.14,
    'A2'  : -0.15,
    '83s' : -0.15,
    '94s' : -0.15,
    '72s' : -0.15,
    '32s' : -0.15,
}

def printScore(spec, full=False):
    if not re.match('^['+cards+']{2}[os]?$', spec, re.I):
        print("Bad hand: "+spec, file=sys.stderr)
        return

    spec = spec.upper()
    hand = sorted(spec[0:2], key=lambda x: cards.find(x))

    if hand[0] == hand[1]:
        # pocket pair
        score = max(chen[hand[0]] * 2, 5)

    else:
        # high card
        score = chen[hand[0]]

        # suited
        if spec.endswith('S'):
            score += 2
            hand.append('s')

        # gap deduction
        if gap(hand) == 0:
            if rank(hand[0]) <= 11:
                score += 1
        elif gap(hand) == 1:
            if rank(hand[0]) > 11:
                score -= 1
        elif gap(hand) == 2:
            score -= 2
        elif gap(hand) == 3:
            score -= 4
        elif gap(hand) >= 4:
            score -= 5

        score = max(score, 0)

    spec = ''.join(hand)
    score = math.ceil(score)
    group = sklansky.get(spec, 9)
    category = nelson.get(spec, 9)
    average = (groupEquivalent(score) + group + category + ftr.get(spec, 9))/4

    if full:
        details = '| %-2s  %-2s  %-2s ' % (
            score,
            'S'+str(group),
            'N'+str(category),
        )
    else:
        details = ''

    print('%-3s %s| %-4s | %5.2f' % (
        spec,
        details,
        '----' if average > 8 or ev[spec] < -0.13 else round(average, 2),
        ev[spec],
    ))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        for i, hc in enumerate(cards):
            for lc in cards[i:]:
                printScore(hc+lc)
                if hc != lc:
                    printScore(hc+lc+'s')
    else:
        for arg in argv[1:]:
            printScore(arg, full=True)

    return 0


if __name__ == '__main__':
    sys.exit(main())

