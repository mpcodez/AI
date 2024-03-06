import sys; args = sys.argv[1:]
import time

height, width, numBS = 0, 0, 0
hWords, vWords = [], []
hEmpty = {}

alphabet = 'abcdefghijklmnopqrstuvwyz#'

for i in range(len(args)):
    if ".txt" in args[i]:
        continue
    elif args[i][0].lower() == 'h' or args[i][0].lower() == 'v':
        k = [j for j in range(1, len(args[i])) if args[i][j].lower() in alphabet]
        if k:
            k = k[0]
            startInder = args[i][1:k]
        else:
            k = 0
            startInder = args[i][1:]

        vVals = int(startInder[:startInder.lower().find('x')])
        hVals = int(startInder[startInder.lower().find('x') + 1:])
        if k > 0:
            word = args[i][k:]
        if k == 0:
            word = "#"
        if args[i][0].lower() == 'h':
            hWords.append((vVals, hVals, word))
        if args[i][0].lower() == 'v':
            vWords.append((vVals, hVals, word))
    elif "x" in args[i]:
        arg = args[i]
        height = int(arg[:arg.lower().find('x')])
        width = int(arg[arg.lower().find('x') + 1:])
    elif args[i][0] in '1234567890':
        numBS = int(args[i])

default = ''.join(['-' for i in range(height*width)])
area = height * width
global colls
colls = [[col + (width * n) for n in range(height)] for col in range(width)]
puzzIndexes = [[(row * width) + v for v in range(width)] for row in range(height)] + [[col + (width * n) for n in range(height)] for col in range(width)]
global dictWordLen
dictWordLen = {}
global wordSet
wordSet = set()

def printboard(puzzle, width):
    for ind in range(len(puzzle)):
        if ind % width == 0:
            print('{}'.format(puzzle[ind]), end='')
        elif ind % width == width - 1:
            print('{}\n'.format(puzzle[ind]), end='')
        else:
            print('{}'.format(puzzle[ind]), end='')
    print('\n')


def addVertical(board, vVals, hVals, word, width):
    if board == "": return ""
    wordIndexes = []
    for k in range(len(word)):
        index = (vVals + k)*width + hVals
        if index > len(board)-1:
            return ""
        wordIndexes.append(index)
    newboard = board
    for k in range(len(wordIndexes)):
        if board[wordIndexes[k]] not in ('-', '#'):
            if board[wordIndexes[k]].lower() == word[k].lower():
                continue
            else:
                return ""
        newboard = newboard[:wordIndexes[k]] + word[k] + newboard[wordIndexes[k]+1:]
    return newboard


def addHorizontal(board, vVals, hVals, word, width):
    if board == "": return ""
    startIndInd = vVals*width + hVals
    endInd = startIndInd + len(word)
    if startIndInd//width != (endInd-1)//width:
        return ""
    newboard = board[:startIndInd] + word + board[endInd:]
    return newboard


def setIndex(board, ind, char):
    if board == "":
        return board
    if board[ind] == char:
        return board
    if board[ind] in ('#'):
        return ""
    return board[:ind] + char + board[ind + 1:]


def insertWords(mat, width, hWords, vWords):
    for hWord in hWords:
        vVals, hVals, word = hWord
        mat = addHorizontal(mat, vVals, hVals, word.lower(), width)
    for vWord in vWords:
        vVals, hVals, word = vWord
        mat = addVertical(mat, vVals, hVals, word.lower(), width)
    return mat


def makeSymm(board):
    length = len(board)
    for index in range(length):
        if board[index] == '-' and board[length - 1 - index] == '#':
            board = setIndex(board, index, '#')
        elif board[index] == '#' and board[length - 1 - index] == 'L':
            return ""
    return board

# assembling

def validify(board):
    for lim in puzzIndexes:
        inds = set()
        counterer = 0
        for conts in lim:
            char = board[conts]
            if char == "#":
                if counterer == 2 or counterer == 1:
                    for ind in inds:
                        if board[ind] != "-" or board[area - 1 - ind] != "-":
                            if board[ind] != "#" or board[area - 1 - ind] != "#": return ""
                        board[ind] = "#"
                        board[area - 1 - ind] = "#"
                counterer = 0
                inds = set()
            elif lim[-1] == conts:
                if (counterer == 0 or counterer == 1):
                    for ind in inds:
                        if board[ind] != "-" or board[area - 1 - ind] != "-": return ""
                        board[ind] = "#"
                        board[area - 1 - ind] = "#"
            else:
                inds.add(conts)
                counterer += 1
    return "".join(board)

def fillMultConnect(board, ind, ch):
    if board[ind] == "#": return board
    if ch == 1:
        if board[ind] != "-" or board[area - 1 - ind] != "-": return ""
        if ind > area - 1 - ind:
            board = board[:area - 1 - ind] + "#" + board[area - ind:ind] + "#" + board[ind + 1:]
        elif ind < area - 1 - ind:
            board = board[:ind] + "#" + board[ind + 1:area - 1 - ind] + "#" + board[area - ind:]
        else:
            board = board[:ind] + "#" + board[ind + 1:]
        if ind % width != 0:
            board = fillMultConnect(board, ind - 1, 1)
            if not board: return ""
        if ind + width < area:
            board = fillMultConnect(board, ind + width, 1)
            if not board: return ""
        if ind - width > 0:
            board = fillMultConnect(board, ind - width, 1)
            if not board: return ""
        if (ind % width) != (width - 1):
            board = fillMultConnect(board, ind + 1, 1)
            if not board: return ""
    if ch == 2:
        board = board[:ind] + "#" + board[ind + 1:]
        if ind - width > 0:
            board = fillMultConnect(board, ind - width, 2)
        if ind + width < area:
            board = fillMultConnect(board, ind + width, 2)
        if ind % width != 0:
            board = fillMultConnect(board, ind - 1, 2)
        if ind % width != width - 1:
            board = fillMultConnect(board, ind + 1, 2)
    return board

def checkConnect(board):
    index = board.find("-")
    if index == -1:
        return False
    newboard = fillMultConnect(board, index, 2)
    return any([True for ch in newboard if ch != "#"])

def connect4(board, numBlocks):
    newboard = ""
    while checkConnect(board):
        for index in range(area):
            if board[index] == "-":
                newboard = fillMultConnect(board, index, 1)
                if not newboard or newboard.count("#") > numBlocks: continue
                else:
                    break
        board = newboard
    return board

def findSpace(board):
    empty = set()
    indLims = (area // 2) if area % 2 == 0 else ((area // 2) + 1)
    for ind in range(indLims):
        if board[ind] == "-" and board[area - 1 - ind] == "-":
            empty.add(ind)
    return empty

def assembleRecur(board, numBlocks):
    if board != "":
        newboard = validify([*board])
        if not newboard:
            return ""
        presBlock = newboard.count("#")
        if presBlock > numBlocks:
            return ""
        while newboard != board:
            board = newboard
            newboard = validify([*newboard])
            if not newboard:
                return ""
            presBlock = newboard.count("#")
            if presBlock > numBlocks:
                return ""
        if checkConnect(board):
            return ""
        if presBlock == numBlocks: return board
    for ind in findSpace(board):
        if ind > area - 1 - ind:
            ab = board[:area - 1 - ind] + "#" + board[area - ind:ind] + "#" + board[ind + 1:]
        elif ind < area - 1 - ind:
            ab = board[:ind] + "#" + board[ind + 1:area - 1 - ind] + "#" + board[area - ind:]
        else:
            ab = board[:ind] + "#" + board[ind + 1:]
        nB = assembleRecur(ab, numBlocks)
        if nB:
            return nB
    return ""

# CW2

def createDict(dict):
    wordset = set()
    file = open(args[0])
    global wordSet
    wordSet = wordset
    wordDict = {}
    for word in file.readlines():
        wordToAdd = ''.join(word.split()).lower()
        if len(wordToAdd) >= 3:
            wordset.add(wordToAdd)
            if (len(wordToAdd) not in dictWordLen):
                dictWordLen[len(wordToAdd)] = [wordToAdd]
            else:
                dictWordLen[len(wordToAdd)].append(wordToAdd)
            for charIndex in range(len(wordToAdd)):
                if (wordToAdd[charIndex], charIndex, len(wordToAdd)) not in wordDict:
                    wordDict[(wordToAdd[charIndex], charIndex, len(wordToAdd))] = [wordToAdd]
                else:
                    wordDict[(wordToAdd[charIndex], charIndex, len(wordToAdd))].append(wordToAdd)
    return wordDict


def bruteForce(board, wordDict, wordsInBoard):
    possBoards = findPossibilities(board, wordDict, wordsInBoard)
    if not possBoards:
        return ""
    if "-" not in board:
        return board
    for (possChoice, used) in possBoards:
        boardRecur = possChoice
        printboard(boardRecur, width)
        bF = bruteForce(boardRecur, wordDict, used)
        if bF: return bF
    return ""

def findPossibilities(board, wordDict, wordsInBoard):
    wordsToAdd = []
    bestChoiceH = set()
    initialH = True
    initialV = True
    bestChoiceV = set()
    for i in range(len(board)):
        if board[i] != '#':
            if (i % width) - 1 < 0 or board[i - 1] == '#':
                hWord = findHSpaces(board, i)
                if '-' not in hWord:
                    if hWord not in wordSet:return ""
                if initialH:
                    bestChoiceH = set(dictWordLen[len(hWord)])
                    indH = i
                    initialH = False
                if '-' in hWord:
                    horWordSet = set(dictWordLen[len(hWord)])
                    for index, char in enumerate(hWord):
                        if char != '-':
                            if ((char, index, len(hWord)) not in wordDict) & ((char.lower(),index,len(hWord)) not in wordDict):return ""
                            horWordSet = horWordSet & set(wordDict[(char, index, len(hWord))])
                    if len(horWordSet) == 0:return ""
                    if len(horWordSet) < len(bestChoiceH):
                        bestChoiceH = horWordSet
                        indH = i
            if (i - width) < 0 or board[i - width] == '#':
                vWord = findVSpaces(board, i)
                if '-' not in vWord:
                    if vWord not in wordSet:return ""
                if initialV:
                    bestChoiceV = set(dictWordLen[len(vWord)])
                    indV = i
                    initialV = False
                if '-' in vWord:
                    verticalWordSet = set(dictWordLen[len(vWord)])
                    for index, char in enumerate(vWord):
                            if char != '-':
                                if ((char, index, len(vWord)) not in wordDict) & ((char.lower(),index,len(vWord)) not in wordDict):return ""
                                verticalWordSet = verticalWordSet & set(wordDict[(char, index, len(vWord))])
                    if len(verticalWordSet) == 0:return ""
                    if len(verticalWordSet) < len(bestChoiceV):
                        bestChoiceV = verticalWordSet
                        indV = i
    if len(bestChoiceH) <= len(bestChoiceV):
        for word in bestChoiceH:
            if word in wordsInBoard:continue
            VtempBoard = board
            listHBoard = [*VtempBoard]
            sHInd = indH
            for char in word:
                listHBoard[sHInd] = char
                sHInd += 1
            newHBoard = ''.join(listHBoard)
            wordsToAdd.append((newHBoard, wordsInBoard + [word]))
        return wordsToAdd
    if len(bestChoiceV) < len(bestChoiceH):
        for word in bestChoiceV:
            if word in wordsInBoard:continue
            HtempBoard = board
            listVBoard = [*HtempBoard]
            sVInd = indV
            for char in word:
                listVBoard[sVInd] = char
                sVInd += width
            newVBoard = ''.join(listVBoard)
            wordsToAdd.append((newVBoard, wordsInBoard + [word]))
        return wordsToAdd
    return ""

def findHSpaces(board, inds):
    hIndexList = [inds]
    ind = 1
    while (inds % width) + ind < width and board[inds + ind] != '#':
        hIndexList.append(inds + ind)
        ind += 1
    hWord = ''.join([board[ind] for ind in hIndexList])
    return hWord

def findVSpaces(board, inds):
    vIndexList = [inds]
    ind = 1
    while inds + (width * ind) < len(board) and board[inds + (ind * width)] != '#':
        vIndexList.append(inds + (ind * width))
        ind += 1
    vWord = ''.join([board[ind] for ind in vIndexList])
    return vWord

def main():
    global hEmpty, vEmpty
    sTime = time.time()
    hEmpty = {i: [] for i in range(height)}
    vEmpty = {i: [] for i in range(width)}
    board = insertWords(default, width, hWords, vWords)
    board = validify([*makeSymm(board)])
    board = connect4(board, numBS)
    board = assembleRecur(board, numBS)

    wordLenDict = createDict(args[0])

    finishedBoard = bruteForce(board, wordLenDict, [])
    printboard(finishedBoard, width)
    #print(time.time()-sTime)


if __name__ == '__main__':
    main()

#Medha Pappula, 6, 2026