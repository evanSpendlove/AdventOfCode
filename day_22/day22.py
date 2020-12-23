from collections import deque
from copy import deepcopy

def score(player):
    return sum([(i+1) * player.popleft() for i in range(len(player))])

def playerToString(p):
    return ','.join(map(str, list(p)))

def hashRound(p1, p2):
    return hash((playerToString(p1), "|", playerToString(p2)))

def removeExtra(deck, extra):
    for i in range(extra): deck.popleft()
    return deck

def recursiveCombat(p1, p2):
    cache = set()
    while p1 and p2:
        curRound = hashRound(p1, p2)
        if curRound in cache:
            return p1, 0
        cache.add(curRound)
        top1, top2 = p1.pop(), p2.pop()
        if top1 <= len(p1) and top2 <= len(p2):
            deck1, deck2 = removeExtra(deepcopy(p1), (len(p1)-top1)), removeExtra(deepcopy(p2), (len(p2)-top2))
            _, winIdx = recursiveCombat(deck1, deck2)
        else:
            winIdx = int(top1 < top2)
        winner = [p1, p2][winIdx]
        cardsToAdd = (top1, top2) if winner == p1 else (top2, top1)
        for c in cardsToAdd: winner.appendleft(c)
    return (p1, 0) if p1 else (p2, 1)

def combat(p1, p2):
    while p1 and p2:
        top1, top2 = p1.pop(), p2.pop()
        top, bottom = max(top1, top2), min(top1, top2)
        winner = p1 if top1 > top2 else p2
        winner.appendleft(top)
        winner.appendleft(bottom)
    return p1 if p1 else p2

def parsePlayer(deck):
    player, deck= deque(), list(map(int, deck.split('\n')[1:]))
    for card in deck: player.appendleft(card)
    return player

with open('input.in', 'r') as f:
    deck1, deck2 = f.read().strip().split('\n\n')
    player1, player2 = parsePlayer(deck1), parsePlayer(deck2)
    winner = combat(deepcopy(player1), deepcopy(player2))
    print(f"P1: Final score: {score(winner)}")
    winner, _= recursiveCombat(deepcopy(player1), deepcopy(player2))
    print(f"P2: Final score of recursive combat: {score(winner)}")
