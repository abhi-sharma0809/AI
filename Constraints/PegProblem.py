import sys; args = sys.argv[1:]
index = 0
dotLook = {
0: [(3,1, '/'), (5,2,'\\')],
1: [(6,3, '/'), (8,4, '\\')],
2: [(7,4, '/'), (9,5, '\\')],
3: [(0,1, '/'), (5,4, '-'), (12,7, '\\'), (10,6, '/')],
4: [(11,7, '/'), (13,8, '\\')],
5: [(0,2, '\\'), (3,5, '-'), (12,8, '/'), (14,9, '\\')],
6: [(1,3, '/'),(8,7, '-'), (17, 11, '\\'), (15, 10, '/')],
7: [(2,4, '/'), (9,8, '-'), (18,12, '\\'), (16,11, '/')],
8: [(6,7, '-'),(1,4, '\\'),(17,12, '/'), (19,13, '\\')],
9: [(2,5, '\\'), (20,14, '\\'), (7,8, '-'), (18,13, '/')],
10: [(3, 6, '/'), (12, 11, '-')],
11: [(4, 7, '/'), (13, 12, '-')],
12: [(10, 11, '-'), (14, 13, '-'), (3, 7, '\\'), (5, 8, '/')],
13: [(11, 12, '-'), (4, 8, '\\')],
14: [(5, 9, '\\'), (12, 13, '-')],
15: [(6, 10, '/'), (17, 16, '-')],
16: [(7, 11, '/'), (18, 17, '-'), (9, 12, '/')],
17: [(15, 16, '-'), (19, 18, '-'), (6, 11, '\\'), (8, 12, '/')],
18: [(7, 12, '\\'), (16, 17, '-'), (20, 19, '-'), (9, 13, '/')],
19: [(17, 18, '-'), (8, 13, '\\')],
20: [(18, 19, '-'), (9, 14, '\\')]
}

def neighbors(puzzle):
    #return a list of all the neighbors of pz
    neighborList = []
    for i, ch in enumerate(puzzle):
        if ch == '.':
            for tp in dotLook.get(i):
                if puzzle[tp[0]]=='1' and puzzle[tp[1]]=='1':
                    newpzl = list(puzzle)
                    newpzl[tp[0]] = '.'
                    newpzl[tp[1]] = '.'
                    newpzl[i] = '1'
                    neighborList.append("".join(newpzl))
    return neighborList



def isFinished(puzzle):
    return puzzle.count('1')==1 and puzzle[index] == '1'

def solve(puzzle):
    #get to the goal in the shortest amount of steps
    #return the number of steps
    if isFinished(puzzle):  
        return puzzle
    parseMe = [puzzle]
    dctSeen = {puzzle: ''}
    for itm in parseMe:
        nextItm = itm
        for n in neighbors(nextItm):
            if n not in dctSeen:
                if(isFinished(n)):
                    dctSeen[n] = nextItm
                    return shortestPath(dctSeen, puzzle, n)
                parseMe.append(n)
                dctSeen[n] = nextItm
    return []

def shortestPath(path, puzzle, goal):
    shortest = []
    current = goal

    while current != puzzle:
        shortest.append(current)
        current = path.get(current)
    shortest.append(puzzle)
    return shortest[::-1]

if(args):
    print(solve(args[0]))
else:
    print(solve('.11111111111111111111'))

#Abhi Sharma and Hriday Sainathuni, pd.7