import sys; args = sys.argv[1:]
import time

class SudokuSolver:
    def __init__(self, puzzle):
        self.board = [[0] * 9 for _ in range(9)]
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]
        self.to_solve = []
        self.parse_puzzle(puzzle)

    def parse_puzzle(self, puzzle):
        for i in range(9):
            for j in range(9):
                num = puzzle[i * 9 + j]
                if num != '.':
                    self.place_number(i, j, int(num))

    def place_number(self, row, col, num):
        self.board[row][col] = num
        self.rows[row].add(num)
        self.cols[col].add(num)
        box_idx = (row // 3) * 3 + col // 3
        self.boxes[box_idx].add(num)

    def remove_number(self, row, col, num):
        self.board[row][col] = 0
        self.rows[row].remove(num)
        self.cols[col].remove(num)
        box_idx = (row // 3) * 3 + col // 3
        self.boxes[box_idx].remove(num)

    def is_valid_move(self, row, col, num):
        return (
            num not in self.rows[row] and
            num not in self.cols[col] and
            num not in self.boxes[(row // 3) * 3 + col // 3]
        )

    def find_empty(self):
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    possibilities = self.get_possibilities(i, j)
                    empty_cells.append((i, j, possibilities))
        empty_cells.sort(key=lambda x: len(x[2]))
        return empty_cells

    def get_possibilities(self, row, col):
        used_numbers = self.rows[row].union(self.cols[col]).union(
            self.boxes[(row // 3) * 3 + col // 3]
        )
        return [n for n in range(1, 10) if n not in used_numbers]

    def solve(self):
        empty_cells = self.find_empty()
        if not empty_cells:
            return True

        row, col, possibilities = empty_cells[0]
        for num in possibilities:
            if self.is_valid_move(row, col, num):
                self.place_number(row, col, num)
                if self.solve():
                    return True
                self.remove_number(row, col, num)

        return False

    def to_string(self):
        return ''.join([str(self.board[i][j]) for i in range(9) for j in range(9)])

def solve_sudoku(puzzle):
    solver = SudokuSolver(puzzle)
    if solver.solve():
        return solver.to_string()
    else:
        return "No solution found."


if __name__ == "__main__":
    puzzles = open(args[0]).read().split("\n")

    count = 1

    for board in puzzles:

        solution = solve_sudoku(board)
        
        startTime = time.time()
        print(f"{count}: {board}")
        spaces = " "*len(str(count) + ": ")
        print(f"{spaces}{solution} 324 {round(time.time() - startTime, 2)}s")
        count += 1

# Medha Pappula, 6, 2026


"""

Ways to Improve:

- Find Best Dot (expand max() comprehension), one with least amount of possible choices
- Bail out of looping through choices if there is only 1 choice
- Bail out of looping through all choices if first doesn't work, and there's only 2 choices

- Possibles/Excluded: Create at the start, add used values as you go.
    - Save all changes, don't create a deep copy, redo all changes
    - Shallow Copy, newPsbl = [*psbl], create a deep copy only for the ones you change


"""