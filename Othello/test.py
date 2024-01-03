import o4

board = '.'*27 + 'ox......xo' + '.'*27
mv = o4.quickMove(board,"x")
print(f"For the board {board} quickMove is {mv}")