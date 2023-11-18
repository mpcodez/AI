def print_sudoku(sudoku_str):
    for i in range(9):
        for j in range(9):
            print(sudoku_str[i * 9 + j], end=" ")
        print()

def is_valid_move(sudoku_str, row, col, num):
    # Check if the number is not present in the same row, column, or block
    return (
        all(num != int(sudoku_str[row * 9 + j]) for j in range(9))
        and all(num != int(sudoku_str[i * 9 + col]) for i in range(9))
        and all(
            num != int(sudoku_str[i * 9 + j])
            for i in range(row - row % 3, row - row % 3 + 3)
            for j in range(col - col % 3, col - col % 3 + 3)
        )
    )

def solve_sudoku(sudoku_str):
    empty = sudoku_str.find('.')
    if empty == -1:
        return sudoku_str  # Puzzle is solved

    row, col = divmod(empty, 9)

    for num in map(str, range(1, 10)):
        if is_valid_move(sudoku_str, row, col, int(num)):
            new_sudoku = sudoku_str[:empty] + num + sudoku_str[empty + 1:]
            solution = solve_sudoku(new_sudoku)

            if solution:
                return solution  # If the current move leads to a solution, return the solution

    return None  # No valid moves, backtrack further

def apply_advanced_strategies(sudoku_str):
    while True:
        # Apply advanced strategies here

        # Break the loop if no changes are made
        if sudoku_str == new_sudoku_str:
            break

    return sudoku_str

# Example Sudoku puzzle in the form of a string
sudoku_str = "...5..2..4......8....1........6..1.57...3..........9...2...8.3..1..7......5......"

# Apply advanced strategies to the Sudoku string
sudoku_str = apply_advanced_strategies(sudoku_str)

# Solve the Sudoku puzzle
solution = solve_sudoku(sudoku_str)

# Print the solved Sudoku puzzle
print_sudoku(solution)
