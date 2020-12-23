from collections import deque
from copy import deepcopy

def score(player):
    return sum([(i+1) * player.popleft() for i in range(len(player))])

def playerToString(p):
    return ','.join(map(str, list(p)))

def hashRound(p1, p2):
    return hash((playerToString(p1), "|", playerToString(p2)))

def removeExtra(deck, extra):
    for i in range(extra):
        deck.popleft()
    return deck

def recursiveCombat(p1, p2, gameID):
    roundCounter = 1
    cache = set()       # Set of tuples where t[0] = p1, t[1] = p2
    while p1 and p2:
        # print(f"--- Round {roundCounter} - Game {gameID} ---")
        # print(f"Player 1: {p1}")
        # print(f"Player 2: {p2}")
        curRound = hashRound(p1, p2)
        if curRound in cache:
            # print('woo')
            return p1, 1
        cache.add(curRound)
        top1, top2 = p1.pop(), p2.pop()
        # print(f"Player 1 plays: {top1}")
        # print(f"Player 2 plays: {top2}")
        if top1 <= len(p1) and top2 <= len(p2):
            # print('Recur')
            deck1, deck2 = deepcopy(p1), deepcopy(p2)
            deck1, deck2 = removeExtra(deck1, (len(p1)-top1)), removeExtra(deck2, (len(p2)-top2))
            assert(len(deck1) == top1)
            assert(len(deck2) == top2)
            _, winIdx = recursiveCombat(deck1, deck2, gameID+1)    # here's my issue!
            winner = p1 if winIdx == 1 else p2
            # print(f"Player {winIdx} wins this recursive round!")
        else:
            winIdx = 1 if top1 > top2 else 2
            # print(f"Player {winIdx} wins this round!")
            winner = p1 if top1 > top2 else p2
        if winner == p1:
            p1.appendleft(top1)
            p1.appendleft(top2)
        if winner == p2:
            p2.appendleft(top2)
            p2.appendleft(top1)
        roundCounter += 1
        # print()
    assert(len(p1) == 0 or len(p2) == 0)
    return (p1, 1) if p1 else (p2, 2)

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
    for card in deck:
        player.appendleft(card)
    return player

with open('input.in', 'r') as f:
    deck1, deck2 = f.read().strip().split('\n\n')
    player1, player2 = parsePlayer(deck1), parsePlayer(deck2)
    winner = combat(deepcopy(player1), deepcopy(player2))
    print(f"P1: Final score: {score(winner)}")

    winner, _= recursiveCombat(deepcopy(player1), deepcopy(player2), 1)
    print(f"P2: Final score of recursive combat: {score(winner)}")
