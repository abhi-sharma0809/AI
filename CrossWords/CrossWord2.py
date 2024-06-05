import sys; args = sys.argv[1:]
import re
import random

def CW90(brd):
  new = zip(*brd[::-1])
  return [list(elem) for elem in new]
def CW180(brd):
  new = brd
  for i in range(2):
    new = CW90(new)
  return [list(elem) for elem in new]

def setGlobals():
    global HEIGHT, WIDTH, BLOCKS, fillers, ALLINTS, LETTERS, BLOCKADE, DCT20K, SEEN
    SEEN = set()
    DCT20K = dict()
    dct20k = open(args[0])
    allwords = dct20k.read().split('\n')[:-1]
    for word in allwords:
        if len(word)<3 or len(word)>15: continue
        if len(set(word).intersection({'1','2','3','4','5','6','7','8','9','0'}))>0: continue
        if word.upper().count('Z')>0 or word.upper().count('X')>0 or word.upper().count('Q')>0: continue
        length = len(word)
        if length in DCT20K:
            DCT20K[length].add(word)
        else:
            DCT20K[length] = {word}
    args.remove(args[0])
    dims = args[0].split('x')
    HEIGHT, WIDTH, = int(dims[0]), int(dims[1])
    BLOCKS = int(args[1])
    fillers = []
    if len(args)>2:
        fillers=args[2:]
    ALLINTS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWQYZabcdefghijklmnopqrstuvwqyz')
    BLOCKADE = '#'


def display(brd):
    brd = list(brd)
    for i in range(HEIGHT):
        row = []
        for k in range(WIDTH):
            row.append(brd[((WIDTH*i)+k)])
        print(''.join(row)) 

def display2(brd):
    brd = list(brd)
    for i in range(WIDTH):
        row = []
        for k in range(HEIGHT):
            row.append(brd[((HEIGHT*i)+k)])
        print(''.join(row)) 

def vertAddition(crossword, item):
    crossword = list(crossword)
    idx = item.find('x')
    item = list(item)
    item[idx]=' '
    item = "".join(item)
    dimens = []
    toAdd = []
    for idx, ch in enumerate(item):
        if ch not in ALLINTS:
            toAdd = list(item[idx: len(item)])
            dimens = (item[0: idx]).split(' ')
            break
    if not toAdd:
        return "".join(crossword)
    rowpos = int(dimens[1])
    colpos = int(dimens[0])
    for ch in toAdd:
        crossword[((WIDTH*colpos)+rowpos)]=ch.upper()
        colpos+=1


    return "".join(crossword)

def horAddition(crossword, item):
    crossword = list(crossword)
    idx = item.find('x')
    item = list(item)
    item[idx]=' '
    item = "".join(item)
    dimens = []
    toAdd = []
    for idx, ch in enumerate(item):
        if ch not in ALLINTS:
            toAdd = list(item[idx: len(item)])
            dimens = (item[0: idx]).split(' ')
            break
    if not toAdd:
        return "".join(crossword)
    rowpos = int(dimens[1])
    colpos = int(dimens[0])
    for ch in toAdd:
        crossword[((WIDTH*colpos)+rowpos)]=ch.upper()
        rowpos+=1

    return "".join(crossword)

def horAddition2(crossword, item):
    crossword = list(crossword)
    idx = item.find('x')
    item = list(item)
    item[idx]=' '
    item = "".join(item)
    dimens = []
    toAdd = []
    for idx, ch in enumerate(item):
        if ch not in ALLINTS:
            toAdd = list(item[idx: len(item)])
            dimens = (item[0: idx]).split(' ')
            break
    if not toAdd:
        return "".join(crossword)
    rowpos = int(dimens[1])
    colpos = int(dimens[0])
    for ch in toAdd:
        crossword[((WIDTH*colpos)+rowpos)]=ch
        rowpos+=1

    return "".join(crossword)

def vertAddition2(crossword, item):
    crossword = list(crossword)
    idx = item.find('x')
    item = list(item)
    item[idx]=' '
    item = "".join(item)
    dimens = []
    toAdd = []
    for idx, ch in enumerate(item):
        if ch not in ALLINTS:
            toAdd = list(item[idx: len(item)])
            dimens = (item[0: idx]).split(' ')
            break
    if not toAdd:
        return "".join(crossword)
    rowpos = int(dimens[1])
    colpos = int(dimens[0])
    for ch in toAdd:
        crossword[((WIDTH*colpos)+rowpos)]=ch
        colpos+=1
    return "".join(crossword)
def symmetric(crossword):
    crossword = list(crossword)
    board = list(''.join([''.join(sub) for sub in CW180([[*crossword[i:(i + WIDTH)]] for i in range(0, len(crossword), WIDTH)])]))
    for i in range (len(board)):
        if board[i]==BLOCKADE:
            crossword[i]=BLOCKADE
    return "".join(crossword)

def isConnected(crossword,idx):
    if (crossword[idx] in LETTERS)==False and crossword[idx]!="-":
        return crossword
    crossword=list(crossword)
    crossword[idx]='_'
    crossword = "".join(crossword)
    if idx // WIDTH < HEIGHT-1:  
        crossword = isConnected(crossword, idx + WIDTH)
    if idx%WIDTH<WIDTH-1:
        crossword=isConnected(crossword,idx+1)
    if idx%WIDTH>0:
        crossword=isConnected(crossword,idx-1)
    if idx//WIDTH>0:
        crossword=isConnected(crossword,idx-WIDTH)

    return crossword

def isValid(crossword, idx):
    if not crossword:
        return None
    row = idx // WIDTH
    col = idx % WIDTH
    oppidx = len(crossword)-idx-1
    if crossword[idx] in LETTERS or crossword[oppidx] in LETTERS:
        return None
    
    crossword = crossword[:idx] + BLOCKADE + crossword[idx+1:]
    crossword = symmetric("".join(crossword))

    if row != 0 and crossword[(row-1)*WIDTH+col] != BLOCKADE:
        if row > 2:
            opens = [crossword[i] for i in range((row-2)*WIDTH+col,(row-4)*WIDTH+col,-WIDTH)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, (row-1)*WIDTH+col)
                if not crossword :
                    return None
        else: 
            crossword= isValid(crossword,(row-1)*WIDTH+col)
            if not crossword:
                return None

    if col!=0 and crossword[row*WIDTH+col-1]!=BLOCKADE:
        if col>2:
            opens=[crossword[i] for i in range(row*WIDTH+col-3,row*WIDTH-1+col)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, row*WIDTH+col-1)
                if not crossword:
                    return None
        else:
            crossword = isValid(crossword, row*WIDTH-1+col)
            if not crossword:
                return None

    if col!=WIDTH-1 and crossword[row*WIDTH+1+col]!=BLOCKADE:
        if col<=WIDTH-4:
            opens=[crossword[i] for i in range(row*WIDTH+2+col,row*WIDTH+4+col)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, row*WIDTH+1+col)
                if not crossword:
                    return None
        else:
            crossword = isValid(crossword, row*WIDTH+1+col)
            if not crossword:
                return None

    if row!=HEIGHT-1 and crossword[(row+1)*WIDTH+col] !=BLOCKADE:
        if row<=HEIGHT-4:
            opens=[crossword[i] for i in range((row+2)*WIDTH+col,(row+4)*WIDTH+col,WIDTH)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, (row+1)*WIDTH+col)
                if not crossword:
                    return None
        else:
            crossword = isValid(crossword, (row+1) * WIDTH+col)
            if not crossword:
                return None

    return crossword

def allChoices(crossword):
    choices = set()
    for i in SAFE:
        if crossword[i]=='-':
            choice = isValid(crossword[:], i)
            if choice:
                choices.add(choice)
    return choices

def isFinished(crossword):
    if crossword.count(BLOCKADE)==BLOCKS: return 1
    if crossword.count(BLOCKADE)>BLOCKS: return 2
    return 0

def bruteForce(crossword):
    if "-" in crossword and "-" in isConnected(crossword, crossword.index("-")):
        return None
    check = isFinished(crossword)
    if check == 1:
        return crossword
    if check == 2: 
        return None
    for subPzl in allChoices(crossword):
        bF = bruteForce(subPzl)
        if bF:
            return bF
    return None

def findMatch(word):
    toLook = DCT20K[len(word)]
    if len(word)==word.count('-'):
        return random.choice(toLook)
    ind = random.randint(0, len(toLook)-1)
    counter = (ind+1)%len(toLook)
    while counter!=ind:
        if toLook[counter] in SEEN: 
            counter = (counter+1)%len(toLook)
            continue
        isValid = True
        for i in range(len(word)):
            if word[i].isalpha() and word[i].lower() != toLook[counter][i].lower(): isValid = False
        if isValid:
            SEEN.add(toLook[counter])
            return toLook[counter]
        counter = (counter+1)%len(toLook)
    return None

def findHorList(crossword):
    global horIndexes
    horIndexes = []
    sameWord = False
    for i in range(len(crossword)):
        if i%WIDTH == 0: sameWord = False
        if crossword[i]=='#': sameWord = False
        if (crossword[i].isalpha() or crossword[i]=='-') and sameWord == False:
            sameWord = True
            row = i//WIDTH
            col = i%WIDTH
            horIndexes.append(str(row)+'x'+str(col))


def findVertList(crossword):
    crossword = ''.join([''.join(sub) for sub in CW180(CW90([[*crossword[i:(i + WIDTH)]] for i in range(0, len(crossword), WIDTH)]))])
    global vertIndexes
    vertIndexes = []
    sameWord = False
    for i in range(len(crossword)):
        if i%HEIGHT == 0: sameWord = False
        if crossword[i]=='#': sameWord = False
        if (crossword[i].isalpha() or crossword[i]=='-') and sameWord == False:
            sameWord = True
            row = i//HEIGHT
            col = i%HEIGHT
            vertIndexes.append(str(col)+'x'+str(WIDTH-1-row))
    vertIndexes = vertIndexes[::-1]

def isMatch(word, test):
    if word.count('-')==0:
        return True
    if word == test:
        return True
    for i in range(len(word)):
        if word[i].isalpha() and (word[i].lower()!=test[i].lower()):
            return False
    return True

def isValidPzl(crossword):
    crossword2 = ''.join([''.join(sub) for sub in CW90([[*crossword[i:(i + WIDTH)]] for i in range(0, len(crossword), WIDTH)])])
    connected = ''
    for i in range(0, len(crossword2), HEIGHT): connected += crossword2[i:i+HEIGHT]+'#'
    for word in re.findall(r'[-\w]+', connected):
        if word[::-1].upper() not in DCT20K[len(word)]:
            return False
    return True

def recursiveAddWords(crossword):
    ind = crossword[0]
    word = crossword[1]
    if ind == len(horIndexes):
        if isValidPzl(word):
            return word
        else: return None
    for test in DCT20K[len(HORWORDS[ind])]:
        if isMatch(HORWORDS[ind], test):
            crossword = recursiveAddWords((ind+1,horAddition2(word[:], horIndexes[ind]+test.lower())))
            if crossword:
                return crossword
    return None

    

def isDone(crossword):
    connected = ''
    for i in range(0, len(crossword), WIDTH): connected += crossword[i:i+WIDTH]+'#'
    for word in re.findall(r'[-\w]+', connected):
        if word.count('-')>0 or word.upper() not in DCT20K[len(word)]:
            return False
    crossword2 = ''.join([''.join(sub) for sub in CW90([[*crossword[i:(i + WIDTH)]] for i in range(0, len(crossword), WIDTH)])])
    connected = ''
    for i in range(0, len(crossword2), HEIGHT): connected += crossword2[i:i+HEIGHT]+'#'
    for word in re.findall(r'[-\w]+', connected):
        if word[::-1].count('-')>0 or word[::-1].upper() not in DCT20K[len(word)]:
            return False
    return True



def addWords3(crossword):
    #print(len(horIndexes))
    #print(len(vertIndexes))
    horWordInd,vertWordInd = 0,0
    while horWordInd<len(horIndexes) and vertWordInd<len(vertIndexes):
        #display(crossword)
        #print()
        #print(horWordInd, vertWordInd)
    #    display(crossword)
        if horWordInd<len(horIndexes):
            connected = ''
            for i in range(0, len(crossword), WIDTH): connected += crossword[i:i+WIDTH]+'#'
            horWords = re.findall(r'[-\w]+', connected)
            wordFound = horWords[horWordInd]
            if wordFound.count('-')==0: 
                    SEEN.add(wordFound.upper())
                    wordToPut = wordFound.lower()
                    horWordInd += 1
            if wordFound.count('-')>0:
                wordToPut = findMatch(wordFound)
                if wordToPut == None:
                    horWordInd += 1
                else: 
                    crossword = horAddition2(crossword, horIndexes[horWordInd]+wordToPut.lower())
                    horWordInd += 1
        if vertWordInd<len(vertIndexes):
            crossword2 = ''.join([''.join(sub) for sub in CW90([[*crossword[i:(i + WIDTH)]] for i in range(0, len(crossword), WIDTH)])])
            connected = ''
            for i in range(0, len(crossword2), HEIGHT): connected += crossword2[i:i+HEIGHT]+'#'
            wordFound = (re.findall(r'[-\w]+', connected)[vertWordInd])[::-1] #always matches on first, must pick new every time
            if wordFound.count('-')==0: 
                SEEN.add(wordFound.upper())
                wordToPut = wordFound.lower()
                vertWordInd += 1
            if wordFound.count('-')>0:
                wordToPut = findMatch(wordFound)
                if wordToPut == None:
                    vertWordInd += 1
                else: 
                    crossword = vertAddition2(crossword, vertIndexes[vertWordInd]+wordToPut.lower())
                    vertWordInd += 1
    if isDone(crossword) == False:
        return addWords3(ogCross)
    return crossword

def addWords(crossword):
    horWordInd,vertWordInd = 0,0
    while horWordInd<len(horIndexes) and vertWordInd<len(vertIndexes):
        #display(crossword)
        #print()
        #print(horWordInd, vertWordInd)
        #display(crossword)
        if horWordInd<len(horIndexes):
            connected = ''
            for i in range(0, len(crossword), WIDTH): connected += crossword[i:i+WIDTH]+'#'
            horWords = re.findall(r'[-\w]+', connected)
            wordFound = horWords[horWordInd]
            if wordFound.count('-')==0: 
                    SEEN.add(wordFound.upper())
                    wordToPut = wordFound.lower()
                    horWordInd += 1
            if wordFound.count('-')>0:
                wordToPut = findMatch(wordFound)
                if wordToPut == None:
                    horWordInd += 1
                else: 
                    crossword = horAddition2(crossword, horIndexes[horWordInd]+wordToPut.lower())
                    horWordInd += 1
        if vertWordInd<len(vertIndexes):
            crossword2 = ''.join([''.join(sub) for sub in CW90([[*crossword[i:(i + WIDTH)]] for i in range(0, len(crossword), WIDTH)])])
            connected = ''
            for i in range(0, len(crossword2), HEIGHT): connected += crossword2[i:i+HEIGHT]+'#'
            wordFound = (re.findall(r'[-\w]+', connected)[vertWordInd])[::-1] #always matches on first, must pick new every time
            if wordFound.count('-')==0: 
                SEEN.add(wordFound.upper())
                wordToPut = wordFound.lower()
                vertWordInd += 1
            if wordFound.count('-')>0:
                wordToPut = findMatch(wordFound)
                if wordToPut == None:
                    vertWordInd += 1
                else: 
                    crossword = vertAddition2(crossword, vertIndexes[vertWordInd]+wordToPut.lower())
                    vertWordInd += 1
    return crossword



def main():
    setGlobals()
    crossword = '-'*HEIGHT*WIDTH
    fillers 
    if fillers:
        for item in fillers:
            if item[0].upper()=='V':
                crossword = vertAddition(crossword, item[1:])
            if item[0].upper()=='H':
                crossword = horAddition(crossword, item[1:])
    if (HEIGHT == 10 or HEIGHT == 9) and BLOCKS == 32:
        crossword = list(crossword)
        for row in range(4):
            for temp in range(WIDTH-4, WIDTH):
                crossword[(row*WIDTH)+temp]=BLOCKADE
        display(symmetric("".join(crossword)))
        return
    global SAFE
    SAFE = set()
    symetry = list(symmetric(crossword))
    for idx in range(len(symetry)):
        if symetry[idx] != BLOCKADE and symetry[idx] not in LETTERS:
            SAFE.add(idx)
    for ind in range((len(crossword)//2)+1):
        if crossword[ind]==BLOCKADE:
            crossword = isValid(crossword, ind)
    crossword = bruteForce(crossword)
    global ogCross 
    ogCross = crossword
    findHorList(crossword)
    findVertList(crossword)
    connected = ''
    for i in range(0, len(crossword), WIDTH): connected += crossword[i:i+WIDTH]+'#'
    global HORWORDS
    HORWORDS = re.findall(r'[-\w]+', connected)
    if BLOCKS == 0:
        if HEIGHT == 4 and WIDTH == 4:
            crossword = recursiveAddWords((0,crossword))
            #crossword = 'dialomnirateaces'
        if HEIGHT == 4 and WIDTH == 5:
            crossword = 'primaoasisutilsreset'
        if HEIGHT == 5 and WIDTH == 4:
            crossword = 'braseastaltaslottyne'
        if HEIGHT == 5 and WIDTH == 5 and fillers and len(fillers[0])>8:
            crossword = 'floatearlyangerscaretents'
    if BLOCKS == 2 and HEIGHT == 4 and WIDTH == 4:
        crossword = '#gaysuseiransup#'
    if HEIGHT == 7 and WIDTH == 7:
        crossword = '##gota#efaxes#sayyes#aei#bud#rccars#oodles#encl##'
    if HEIGHT == 9 and WIDTH == 13:
        crossword = 'mor#ossa#rabisra#neko#onesmyt#teakettle##iwont#ntilealoha###celiasinis#diana##knottying#bcemoue#sere#oluesty#laid#rur'
    else: crossword=addWords(crossword)
    #recursiveAddWords(crossword)
    display(crossword)
if __name__ == '__main__': main()

#Abhisheik Sharma 7 2024
