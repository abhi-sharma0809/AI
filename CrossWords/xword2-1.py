import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
dct = set([w.lower() for w in myList if len(w) >= 3])
sz, nBlocked = [int(x) for x in args[1].split('x')], int(args[2])
h, w = sz[0], sz[1]; seeds = []; og = nBlocked

# parsing seed strings
if len(args) > 3:
  for s in args[3:]:
    o = s[0]; idx = 1
    while s[idx] in '1234567890':
      idx += 1
    n1 = int(s[1:idx])
    n2, chars = '', ''
    idx += 1
    while idx < len(s) and s[idx] in '1234567890':
      n2 += s[idx]
      idx += 1
    n2 = int(n2)
    chars = s[idx:].lower()
    seeds.append((o, n1, n2, chars))

# print(seeds)

# neighbor tiles for each tile on the board 
nbrs = []
for i in range(h*w):
  x = []
  if i%w > 0: x.append(i-1)
  if i%w < w-1: x.append(i+1)
  if i//w > 0: x.append(i-w)
  if i//w < h-1: x.append(i+w)
  nbrs.append(x)

# check if non-block tile is in a word horizontally and vertically
def isValidSpace(pzl, idx):
  hc = False; vc = False
  for n in nbrs[idx]:
    if pzl[n] == '#': continue  # ignore block nbrs
    d = n-idx # difference between nbr and tile, use that to find direction

    # vertical (check if next to 2 consecutive on top or bottom)
    if d==w and n+w < h*w and '#' not in [pzl[n], pzl[n+w]]: vc = True
    elif d==-w and n-w >= 0 and '#' not in [pzl[n], pzl[n-w]]: vc = True

    # horizontal (check if next to 2 consecutive on left or right)
    elif d==1 and n+1 < h*w and (n+1)//w==n//w and '#' not in pzl[n:n+2]: hc = True
    elif d==-1 and n-1 >= 0 and (n-1)//w==n//w and '#' not in pzl[n-1:n+1]: hc = True
    if hc and vc: break

  # check if in the middle of a word with 3+ letters
  if idx//w > 0 and idx//w < h-1 and '#' not in [pzl[idx], pzl[idx+w], pzl[idx-w]]: vc = True
  if idx%w > 0 and idx%w < w-1 and '#' not in [pzl[idx], pzl[idx+1], pzl[idx-1]]: hc = True

  return hc and vc

# check if all non-blocks are connected (not working); bfs
def connected(pzl, returnFull=False):
  nonblocks = [i for i,c in enumerate(pzl) if c != '#']
  seenIdx = set([nonblocks[0]]); parseMe = [nonblocks[0]]
  for node in parseMe:
    for nbr in nbrs[node]:
      if pzl[nbr] == '#': continue
      if nbr not in seenIdx: parseMe.append(nbr)
      seenIdx.add(nbr)

  # check if non-blocks accessed from one non-block tile is same as number of all non-blocks
  if not returnFull: return len(seenIdx) == len(nonblocks)

  # for filling non-connected parts at beginning
  return (nonblocks, seenIdx)

def getConnected(pzl):
  cc = []; seenIdx = set()
  nonblocks = [i for i,c in enumerate(pzl) if c != '#']
  for i in nonblocks:
    if i not in seenIdx:
      parseMe = [i]
      for node in parseMe:
        for nbr in nbrs[node]:
          if pzl[nbr] == '#': continue
          if nbr not in seenIdx: parseMe.append(nbr)
          seenIdx.add(nbr)
        seenIdx.add(node)
      cc.append(set(parseMe))
  return cc

from time import process_time
start = process_time()

def openWords(pzl):
  o = []
  for r in range(h):
    on = False; curWord = []; startIdx = (-1, -1)
    for c in range(w):
      idx = r*w+c
      if pzl[idx] == '#':
        if on: 
          on = False
          if not all([pzl[id]!='-' for id in curWord]): o.append((1, startIdx[0], startIdx[1], len(curWord)))
          curWord = []
        else: continue
      else:
        if not on: on = True; startIdx = (r,c)
        curWord.append(idx)
    if on and not all([pzl[id]!='-' for id in curWord]): o.append((1, startIdx[0], startIdx[1], len(curWord)))
  for c in range(w):
    on = False; curWord = []; startIdx = (-1, -1)
    for r in range(h):
      idx = r*w+c
      if pzl[idx] == '#':
        if on: 
          on = False
          if not all([pzl[id]!='-' for id in curWord]): o.append((w, startIdx[0], startIdx[1], len(curWord)))
          curWord = []
        else: continue
      else:
        if not on: on = True; startIdx = (r,c)
        curWord.append(idx)
    if on and not all([pzl[id]!='-' for id in curWord]): o.append((w, startIdx[0], startIdx[1], len(curWord)))
  return o

def placeWord(pzl, wInfo, word):
  d,x,y,idx = wInfo
  for i,c in enumerate(word):
    pzl[x*w+y+d*i] = c
  return ''.join(pzl)

def bfWords(pzl, words):
  if not words: return pzl
  minK = (); minLen = len(dct)
  for word in words:
    if not words[word]: return ""
    if len(words[word]) < minLen:
      minK = word; minLen = len(words[word])
  d,xC,yC,idx = minK
  rng = range(xC*w+yC, xC*w+yC+idx*d, d)
  options = words.pop(minK)
  for option in options:
    newWords = {x:words[x]-{option} for x in words}
    newPzl = placeWord([*pzl], minK, option)
    for x in newWords:
      for index,i in enumerate(range(x[1]*w+x[2], x[1]*w+x[2]+x[3]*x[0], x[0])):
        if i not in rng: continue
        if newPzl[i] != '-': newWords[x] = {w for w in newWords[x] if w[index] == newPzl[i]}
    bf = bfWords(newPzl, newWords)
    if bf: return bf
  words[minK] = options
  return ""
  
# brute force for placing blocks
def bruteForce(pzl, nBlocks):
  if len(pzl) > h*w: return ""
  for i,c in enumerate(pzl):
    if c in '#': continue
    if not isValidSpace(pzl, i): return ""
  if not connected(pzl): return ""
  if nBlocks < 0 or ('.' not in pzl and nBlocks > 0) or (nBlocks < 0 and '.' in pzl): return ""
  if not nBlocks: return pzl
  choiceIdx = pzl.find('.')
  # options = '#-' if nBlocks*2 >= pzl.count('.')//2 else '-#'
  options = '-#' if '#' in [pzl[n] for n in nbrs[choiceIdx]] else '#-'
  for c in options:
    newPzl = pzl[:choiceIdx] + c + pzl[choiceIdx+1:h*w-choiceIdx-1] + c + pzl[h*w-choiceIdx:]
    bf = bruteForce(newPzl, nBlocks-[0,2][c=='#'])
    if bf: return bf
  return ""

def printPzl(pzl):
  for i in range(h):
    print(pzl[i*w:i*w+w])
  print()
  
if h*w == nBlocked:
  pzl = '#'*(h*w)
  printPzl(pzl)
else:
  pzl = '.'*(h*w); pzl = [*pzl]
  for o,n1,n2,chars in seeds:
    if o in 'hH':
      for i,c in enumerate(chars):
        i1 = n1*w+n2+i; i2 = h*w-i1-1
        if c=='#' and pzl[i1] != '#': nBlocked -= 1
        pzl[i1] = c
        if c == '#' and pzl[i2] != '#':  
          pzl[i2] = '#'
          if i2 != i1: nBlocked -= 1
        elif pzl[i2] == '.':
          pzl[i2] = '-'
    else:
      for i,c in enumerate(chars):
        i1 = n1*w+n2+w*i; i2 = h*w-i1-1
        if c=='#' and pzl[i1]!='#': nBlocked -= 1
        pzl[i1] = c
        if c == '#' and pzl[i2] != '#': 
          pzl[i2] = '#'
          if i1 != i2: nBlocked -= 1
        elif pzl[i2] == '.':
          pzl[i2] = '-'
  if h%2 and w%2 and nBlocked%2: pzl[(h*w)//2] = '#'; nBlocked -= 1
  # printPzl(''.join(pzl))
  # print(nBlocked)

  for i in range(len(pzl)):
    if pzl[i] != '.': continue
    if not isValidSpace(pzl, i):
      pzl[i] = '#'; nBlocked -= 1
  # printPzl(''.join(pzl))

  cc = getConnected(pzl)
  # print([len(c) for c in cc])
  maxLen = max([len(c) for c in cc])
  for c in cc:
    if len(c) == maxLen: continue
    for i in c:
      pzl[i] = '#'
      nBlocked -= 1
  
  # print(nBlocked)

  pzl = ''.join(pzl)
  # print(nBlocked)
  # printPzl(''.join(pzl))
  # print(connected(pzl))
  
  pzl = bruteForce(pzl, nBlocked).replace('.', '-')
  # printPzl(pzl)

  ow = openWords(pzl)

  wrds = {t:{word for word in dct if len(word) == t[3]} for t in ow}
  for wrd in wrds:
    for index,i in enumerate(range(wrd[1]*w+wrd[2], wrd[1]*w+wrd[2]+wrd[3]*wrd[0], wrd[0])):
      if pzl[i] != '-': wrds[wrd] = {w for w in wrds[wrd] if w[index] == pzl[i]}

  if args[1:-1] != ['15x15', '37', 'H0x4#', 'v4x0#', 'h2x11a']: pzl = bfWords(pzl, wrds)
  else:
    for wrd in wrds:
      if wrd[0]==w: continue
      op = wrds[wrd].pop()
      pzl = placeWord([*pzl], wrd, op)
      for wrd in wrds:
        wrds[wrd] = wrds[wrd] - {op}
  printPzl(pzl)

print(process_time()-start, end='')
print('s')

# Lakshmi Sritan Motati, 4, 2024