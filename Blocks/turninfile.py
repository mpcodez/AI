import sys; args = sys.argv[1:]

def setup(pieces):

    items = []
    tmp = ""
    add = False
    for x in pieces:
        if x == " " and add == True:
            items.append(tmp)
            tmp = ""
            add = False
            continue
        elif x == " ":
            tmp += "X"
            add = True
            continue

        if x == "x" or x == "X":
            add = True
            tmp += "X"
            continue
        
        tmp += x

    items.append(tmp)

    blocks = []

    for i in items:
        tmp = i.split("X")
        blocks.append((int(tmp[0]), int(tmp[1])))

    board = blocks[0]
    blocks = blocks[1:]

    return board[0], board[1], blocks

def place_piece(filled,height,width):
    index = filled.index(" ")
    if index % puzzle_width + width > puzzle_width: #no space on right
        return None,None
    if index // puzzle_width + height > puzzle_height: #no space on bottom
        return None,None
    for h in range(index,index+puzzle_width*height,puzzle_width): #already filled
        if "x" in filled[h:h+width]:
            return None,None
        filled=filled[:h]+ "x"*width + filled[h+width:]
    tup=(index//puzzle_width,index%puzzle_width,height,width)
    return tup,filled


def solve(used,filled,rects):
    if " " not in filled:
        return used
    next_piece=rects[-1]
    for next_piece in rects:
        tup,new_filled=place_piece(filled,next_piece[0],next_piece[1]) #trying 1st orientation
        new_rects=rects.copy()
        new_rects.remove(next_piece)
        if new_filled is not None:
            new_used=solve(used+[tup],new_filled,new_rects)
            if new_used is not None:
                return new_used
        tup,new_filled=place_piece(filled,next_piece[1],next_piece[0]) #trying 2nd orientation
        if new_filled is not None:
            new_used = solve(used+[tup], new_filled, new_rects)
            if new_used is not None:
                return new_used
    return None

inpt = " ".join(args)
puzzle_height, puzzle_width, rectangles = setup(inpt)
used = solve([]," "*(puzzle_width*puzzle_height),rectangles.copy())
if used==None:
    print("Impossible")
else:
    retStr = ""
    for item in used:
        retStr += "(" + str(item[2]) + ", " + str(item[3]) + "), "
    print("Decomposition: [" + retStr[:len(retStr)-2] + "]")

# Medha Pappula, 6, 2026