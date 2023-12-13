import sys; args = sys.argv[1:]

def print_board(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))

def print_possible_moves(board, poss_moves):
    print_board(''.join([ch if idx not in poss_moves else '*' for idx, ch in enumerate(board)]))

def next_tokens(board):
    if board.count('.') % 2:
        return 'o', 'x'
    return 'x', 'o'

def get_opp_token(token):
    return 'o' if token == 'x' else 'x'

def check_bracketing(token, poss_ind, adj_ind, board):
    subset = SUBSETS[adj_ind][poss_ind]
    return any(board[index] == token for index in subset if board[index] != '.')

def next_moves(board, tokens=''):
    poss_moves = set()

    if tokens == '':
        token, opp_token = next_tokens(board)
    else:
        token, opp_token = tokens, get_opp_token(tokens)

    for idx in NBRS:
        if board[idx] == opp_token:
            for nbr in NBRS[idx]:
                if board[nbr] == '.' and check_bracketing(token, nbr, idx, board):
                    poss_moves.add(nbr)

    return len(poss_moves), poss_moves

default_board = '.'*27 + "ox......xo" + '.'*27
NBRS = {}
SUBSETS = []
start_board = default_board
start_tokens = ''

inpt = args
inpts = len(inpt)

if inpts == 2:
    if len(inpt[0]) == 64:
        start_board = inpt[0].lower()
        start_tokens = inpt[1].lower()
    elif len(inpt[0]) == 1:
        start_tokens = inpt[0]
        start_board = inpt[1].lower()
elif inpts == 1:
    if len(inpt[0]) == 64:
        start_board = inpt[0].lower()
    elif len(inpt[0]) == 1:
        start_tokens = inpt[0].lower()

idxs = [i for i in range(0, len(default_board))]
for index in idxs:
    if index % 8 == 0:
        NBRS[index] = {index + 1, index - 8, index + 8, index - 7, index + 9}.intersection(idxs)
    elif index % 8 == 7:
        NBRS[index] = {index - 1, index - 8, index + 8, index + 7, index - 9}.intersection(idxs)
    else:
        NBRS[index] = {index - 1, index + 1, index - 8, index + 8, index - 7, index + 7, index - 9, index + 9}.intersection(idxs)

for index in idxs:
    sub_dict = {nbr: [] for nbr in NBRS[index]}
    for nbr in NBRS[index]:
        diff = index - nbr
        prev = nbr
        current = nbr + diff
        while -1 < current < 64 and current in NBRS[prev]:
            if current != index:
                sub_dict[nbr].append(current)
            prev = current
            current = current + diff
        if sub_dict[nbr]:
            SUBSETS.append(sub_dict)

NBRS = {index: {key for key in SUBSETS[index]} for index in NBRS}
del_inds = {key for key in NBRS if not NBRS[key]}
for key in del_inds:
    del NBRS[key]

if start_tokens != "" and next_tokens(start_board)[0] != start_tokens:
    print('No moves possible')
else:
    can_move, poss_moves = next_moves(start_board, start_tokens)

    if can_move:
        print(poss_moves)
    else:
        print('No moves possible')

# Medha Pappula, 6, 2026