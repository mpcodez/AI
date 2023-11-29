blocks = ["17x10 10X17", "17X3 13x3 3 4"]

def decompose(pieces):

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
        for x in range(2):
            tmp[x] = int(tmp[x])
        blocks.append((max(tmp), min(tmp)))

    board = blocks[0]
    blocks = blocks[1:]

    if board == blocks[0]:
        return f"Decomposition: {blocks[0][0]}, {blocks[0][1]}"
    else:
        return "Impossible"

for i in blocks:
    print(decompose(i))

    """
import sys

# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
puzzle = sys.argv[1].split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions



# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
#
# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.
"""