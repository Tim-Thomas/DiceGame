import random

class Die:
    def __init__(self):
        self.value = random.randint(1,6)

    def roll(self):
        self.value = random.randint(1,6)

    def getValue(self):
        return self.value

def scoreAces( hand ):
    return hand.count(1)*1

def score2s( hand ):
    return hand.count(2)*2

def score3s( hand ):
    return hand.count(3)*3

def score4s( hand ):
    return hand.count(4)*4

def score5s( hand ):
    return hand.count(5)*5

def score6s( hand ):
    return hand.count(6)*6

def score3OfaKind( hand ):
    counts = [hand.count(x) for x in range(1,7)]
    if 3 in counts:
        return sum(hand)
    return 0

def score4OfaKind( hand ):
    counts = [hand.count(x) for x in range(1,7)]
    if 4 in counts:
        return sum(hand)
    return 0

def scoreFullHouse( hand ):
    counts = [hand.count(x) for x in range(1,7)]
    if 2 in counts and 3 in counts:
        return 25
    return 0

def scoreSmallStraight( hand ):
    hand.sort()
    diffs = [str(hand[i+1]-hand[i]) for i in range(0,4)]
    diffs = ''.join(diffs)
    diffs = diffs.replace("0", "")
    if "111" in diffs:
        return 30
    else:
        return 0
    

def scoreLargeStraight( hand ):
    hand.sort()
    if [hand[i+1]-hand[i] for i in range(0,4)] == [1,1,1,1]:
        return 40
    return 0

def scoreYahtzee( hand ):
    counts = [hand.count(x) for x in range(1,7)]
    if 5 in counts:
        return 50
    return 0

def scoreChance( hand):
    return sum(hand)
    
