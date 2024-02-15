import sys; args = sys.argv[1:]
import time

LIMIT_AB = 14
num_games = 10
recur_limit = 5
time_limit = 2

corners = [0, 7, 56, 63]
csquares = [(0, 1), (7, 6), (0, 8), (7, 15), (56, 48), (63, 55), (56, 57), (63, 62)]
csquares_worse = [(0, 9), (7, 14), (56, 49), (63, 54)]

row2colb_top = [(-8, j) for j in range(10,14)]
row2colb_bottom = [(8, j) for j in range(50, 54)]
row2colb_left = [(-1, 17 + 8 * j) for j in range(4)]
row2colb_right = [(1, 22 + 8 * j) for j in range(4)]

row2colb = row2colb_top + row2colb_bottom + row2colb_left + row2colb_right

edge_top = [j for j in range(1, 7)]
edge_bottom = [j for j in range(57, 63)]
edge_left = [8 + 8 * j for j in range(6)]
edge_right = [15 + 8 * j for j in range(6)]

edges = edge_top + edge_bottom + edge_left + edge_right

inner_diagonals = [18, 27, 36, 45, 21, 28, 35, 42]

positions = {"corners" : corners, "csquares" : csquares, "csquares_worse" : csquares_worse, \
    "row2colb" : row2colb, "edges": edges, "inner_diagonals" : inner_diagonals}

def main():
    board = '.' * 27 + 'ox......xo' + '.' * 27
    tokenToMove = ''
    oppositeToken = ''
    possible_moves = []
    first_run = args == []

    while args or first_run:
        if args and args[0].startswith('-'):
            args.pop(0)
            continue

        if args and len(args[0]) == 64:
            board = args[0].lower()
            args.pop(0)

        if args and args[0].isalpha():
            tokenToMove = args[0].lower()
            args.pop(0)
        elif not tokenToMove:
            num_tokens = 64 - board.count('.')

            if num_tokens % 2 == 0:
                tokenToMove = 'x'
            else:
                tokenToMove = 'o'

        if args and args[0]:
            if args[0].isdigit():
                temp_move = int(args[0])
                if 0 <= temp_move <= 63:
                    possible_moves.append(temp_move)
                    args.pop(0)
            else:
                if len(args[0]) == 2 and 'a' <= args[0][0].lower() <= 'h' and args[0][1].isdigit() and 0 <= int(args[0][1]) <= 8:
                    possible_moves.append((int(args[0][1]) - 1) * 8 + ord(args[0][0].lower()) - ord('a'))
                    args.pop(0)

        first_run = False

    oppositeToken = 'o' if tokenToMove == 'x' else 'x'

    findBestMove(board, tokenToMove, oppositeToken, LIMIT_AB)


def findBoardValue(board, tokenToMove, oppositeToken):
    num_possible_moves = len(find_or_make_moves(board, tokenToMove, oppositeToken))
    num_player_tok = board.count(tokenToMove)
    num_opp_tok = board.count(oppositeToken)
    total_tok = num_player_tok + num_opp_tok
    curr_player_score = num_player_tok / total_tok
    mobility = 0
    position_score = 0

    score_val = (total_tok / 50) * ((11 ** curr_player_score) - 6) * 1.2

    if num_possible_moves == 0:
        mobility = -24
    elif num_possible_moves == 1:
        mobility = -18
    else:
        mobility = (num_possible_moves ** 1.5) - 8

    for i in positions["corners"]:
        if board[i] == tokenToMove:
            position_score += 4
    
    for i in positions["csquares"]:
        if board[i[0]] != tokenToMove and board[i[1]] == tokenToMove:
            position_score -= 3

    for i in positions["csquares_worse"]:
        if board[i[0]] != tokenToMove and board[i[1]] == tokenToMove:
            position_score -= 4
    
    for i in positions["row2colb"]:
        if board[i[1] + i[0]] != tokenToMove and board[i[0]] == tokenToMove:
            position_score -= 1

    for i in positions["edges"]:
        if board[i] == tokenToMove:
            position_score += 2
    
    for i in positions["inner_diagonals"]:
        if board[i] == tokenToMove:
            position_score += 1

    return score_val + mobility + position_score

# finds the optimal move

def findBestMove(board, tokenToMove, oppositeToken, limitNM, verbose=True):
    moves = find_or_make_moves(board, tokenToMove, oppositeToken)
    ret = None

    final_move = None

    if board.count('.') < limitNM:
        if verbose:
            ret = alphabeta(board, tokenToMove, oppositeToken, -500, 500, 3, start_time=time.time())
            if ret:
                print(ret[-1])

        negamax_output = alphabeta(board, tokenToMove, oppositeToken, -65, 65)

        if not negamax_output:
            if not ret:
                return moves[0]
            else:
                return ret[-1]
        else:
            final_move = negamax_output[-1]
    else:
        prev = None
        # otherwise, run negamax up until a certain limit
        if verbose:
            start = time.time()
            # iterative deepening
            for i in range(1, recur_limit):
                negamax_output = alphabeta(board, tokenToMove, oppositeToken, -500, 500, i, start_time=start)
                
                if negamax_output:
                    prev = negamax_output[-1]
                    #print(negamax_output[-1])

        else:
            start = time.time()
            # iterative deepening
            for i in range(1, recur_limit):
                negamax_output = alphabeta(board, tokenToMove, oppositeToken, -500, 500, i, start_time=start)
                
                if negamax_output:
                    prev = negamax_output[-1]
        
        if negamax_output:
            final_move = negamax_output[-1]
        elif prev:
            final_move = prev
        else:
            final_move = moves[0]
        
    
    tokenThatMoved = tokenToMove

    if verbose:
        # first snapshot 
        final_board = find_or_make_moves(board, tokenToMove, oppositeToken, final_move)

        tokenThatMoved = tokenToMove
        tokenToMove, oppositeToken = oppositeToken, tokenToMove

        tmpBoard = board
        for move in moves:
            tmpBoard = tmpBoard[:move] + '*' + tmpBoard[move+1:]
            
        for i in range(8):
            for j in range(8):
                print(tmpBoard[i * 8 + j], end=' ')
            print()
            
        print(board, str(board.count('x')) + '/' + str(board.count('o')))

        print('Possible moves for', tokenThatMoved + ':', moves)

        print()

        if negamax_output:
            print('Min score: ' + str(negamax_output[0]) + '; move sequence:', *(negamax_output[1:]))
            
    return final_move


def find_or_make_moves(board, tokenToMove, oppositeToken, moveIndex=None):
    moves = []
    tokensToFlip = []
    # left, right, up, down, upleft, upright, downleft, downright
    start = 0
    end = len(board)

    if moveIndex is None and 'x' in board and 'o' in board:
        start = min(board.index('x'), board.index('o'))
        start = max(start - 9, 0)

        end = max(board.rindex('x'), board.rindex('o'))
        end = min(end + 10, len(board))
    # print(tokenToMove, oppositeToken)

    loopBounds = None

    if moveIndex is None:
        loopBounds = (start, end)
    else:
        loopBounds = (moveIndex, moveIndex + 1)

    # current has to be dot, next has to be opposite, keep going in same direction until you reach same token as tokenToMove
    for i in range(*loopBounds):
        curr = board[i]

        if curr == '.':
            completed = False

            # right
            if i % 8 < 6 and board[i + 1] == oppositeToken:
                tempTokensToFlip = [i, i + 1]
                next_idx = i + 2

                while next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 1

            # left
            if i % 8 > 1 and board[i - 1] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 1]
                next_idx = i - 2

                while next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 1

            # up
            if i // 8 > 1 and board[i - 8] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 8]
                next_idx = i - 16

                while next_idx // 8 != -1:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 8

            # down
            if i // 8 < 6 and board[i + 8] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i + 8]
                next_idx = i + 16

                while next_idx // 8 != 8:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 8

            # upleft
            if i // 8 > 1 and i % 8 > 1 and board[i - 9] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 9]
                next_idx = i - 18

                while next_idx // 8 != -1 and next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 9

            # upright
            if i // 8 > 1 and i % 8 < 6 and board[i - 7] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 7]
                next_idx = i - 14

                while next_idx // 8 != -1 and next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 7

            # downleft
            if i // 8 < 6 and i % 8 > 1 and board[i + 7] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i + 7]
                next_idx = i + 14

                while next_idx // 8 != 8 and next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 7

            # downright 
            if i // 8 < 6 and i % 8 < 6 and board[i + 9] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i + 9]
                next_idx = i + 18

                while next_idx // 8 != 8 and next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 9

    if moveIndex is not None:
        updated_board = board

        for i in tokensToFlip:
            updated_board = updated_board[:i] + tokenToMove + updated_board[i + 1:] 
        return updated_board

    return moves

def alphabeta(board, tokenToMove, oppositeToken, raw_lower, upper, level=None, start_time=0):
    # alphabeta should run for a max of 2.5s to not waste too much time (iterative deepening should cover it)
    if (time.time() - start_time <= time_limit) or (start_time == 0):
        lower = raw_lower
        possible_moves = find_or_make_moves(board, tokenToMove, oppositeToken)

        # bottom level, base case

        if level is not None and level <= 0:
            # skip
            if not possible_moves:
                skipped_possible_moves = find_or_make_moves(board, tokenToMove, oppositeToken)

                # if the game is already over

                if not skipped_possible_moves:
                    curr_score = board.count(tokenToMove) - board.count(oppositeToken)
                    # scaled_score = 0.000035 * ((curr_score + 5) ^ 3) - 0.0002 * (curr_score ^ 2) + 0.28 * curr_score
                    return [curr_score]

                else:
                    # just recur one more time

                    result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, 1, start_time=start_time)
                    if result:
                        return [-result[0]] + result[1:] + [-1]
                    else:
                        return

            else:
                # use my heuristic
                ret = findBoardValue(board, tokenToMove, oppositeToken) - findBoardValue(board, oppositeToken, tokenToMove)
                return [ret]


        if not possible_moves:
            # curr token cannot move, pass
            possible_moves = find_or_make_moves(board, oppositeToken, tokenToMove)

            if not possible_moves:
                # double skip or end of game 
                curr_score = board.count(tokenToMove) - board.count(oppositeToken)
                # scaled_score = 0.000035 * ((curr_score + 5) ^ 3) - 0.0002 * (curr_score ^ 2) + 0.28 * curr_score
                return [curr_score]

            result = None
            
            if level is None:
                result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, start_time=start_time)
            else:
                result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, level - 1, start_time=start_time)

            if result:
                return [-result[0]] + result[1:] + [-1]
            else:
                return

        bestSoFar = [lower - 1]

        
        for mv in possible_moves:
            newBrd = find_or_make_moves(board, tokenToMove, oppositeToken, moveIndex=mv)

            if level is None:
                result = alphabeta(newBrd, oppositeToken, tokenToMove, -upper, -lower, start_time=start_time)
            else:
                result = alphabeta(newBrd, oppositeToken, tokenToMove, -upper, -lower, level - 1, start_time=start_time)
                
            if not result:
                return

            score = -result[0]

            if score < lower:
                continue
            if score > upper:
                return [score]

            if score > bestSoFar[0]:
                bestSoFar = [score] + result[1:] + [mv]

            lower = score + 1
            
        return bestSoFar
    
    return

if __name__ == '__main__': 
    main()
    
# Medha Pappula, 6, 2026