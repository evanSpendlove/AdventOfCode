from collections import deque

def score(player):
    return sum([(i+1) * player.popleft() for i in range(len(player))])

def playGame(p1, p2):
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
    winner = playGame(player1, player2)
    print(f"P1: Final score: {score(winner)}")
