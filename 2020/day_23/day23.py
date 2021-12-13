class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

def findDestinationIdx(targetNum, pickedUp, n):
    for i in range(4):
        if targetNum < 1:
            targetNum = n
        if targetNum in pickedUp:
            targetNum -= 1
        else:
            return targetNum
def scoreP1(cups, nodes):
    cur = nodes[1].next
    vals = []
    while cur != nodes[1]:
        vals.append(str(cur.val))
        cur = cur.next
    return ''.join(vals)

def scoreP2(cups, nodes):
    return nodes[1].next.val * nodes[1].next.next.val

def pickThree(cur):
    start, pickedVals = cur, []
    for i in range(3):
        pickedVals.append(cur.val)
        cur = cur.next
    prev = cur.prev
    start.prev.next = cur
    cur.prev = start.prev
    prev.next = None
    return start, pickedVals

def insertAtDestination(destination, pickedUp):
    end = destination.next
    destination.next = pickedUp
    pickedUp.prev = destination
    for i in range(2): pickedUp = pickedUp.next
    pickedUp.next = end
    end.prev = pickedUp

def moveCups(cups, nodes, turnCount, score, n):
    cur = cups
    for i in range(turnCount):
        curVal = cur.val
        pickedUp, pickedVals = pickThree(cur.next)
        destination = nodes[(findDestinationIdx(curVal - 1, pickedVals, n))]
        insertAtDestination(destination, pickedUp)
        cur = nodes[curVal].next
    return score(cups, nodes)

def createList(vals):
    head = Node(vals[0])
    prev = head
    nodes = {cups[0]: head}
    for i in range(1, len(cups)):
        # Create node and dict entry
        cur = Node(cups[i])
        nodes[cups[i]] = cur
        # Doubly link
        prev.next = cur
        cur.prev = prev
        # Update previous node
        prev = cur
    # Make it circular
    head.prev = cur
    cur.next = head
    return head, nodes

with open('input.in', 'r') as f:
    cups = [int(c) for c in f.read().strip()]
    p1_head, p1_nodes = createList(cups)
    print(moveCups(p1_head, p1_nodes, 100, scoreP1, len(cups)))
    for i in range(len(cups)+1, 1000001): cups.append(i)
    p2_head, p2_nodes = createList(cups)
    print(moveCups(p2_head, p2_nodes, 10000000, scoreP2, len(cups)))
