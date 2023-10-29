import sys; args = sys.argv[1:]

gWidth = 4

def rowOfSpace(st):
    return int(st.index("_")/gWidth)

class Queue():
    def __init__(self):
        self.buckets = []

    def enqueue(self, obj, importance):
        if importance < 0:
            raise ValueError("Importance must be a non-negative integer.")
        
        # Ensure there are enough buckets to accommodate the importance value
        while len(self.buckets) <= importance:
            self.buckets.append(set())
        
        self.buckets[importance].add(obj)

    def dequeue(self):
        for bucket in self.buckets:
            if bucket:
                obj = bucket.pop()
                return obj
        return None
        
    def is_empty(self):
        return all(not bucket for bucket in self.buckets)

    def __str__(self):
        return str(self.buckets)

def h(puzzle, goal):
    n = gWidth  # Calculate the size of the puzzle (n x n)
    total_manhattan_distance = 0

    for tile in puzzle:
        if tile != '_':  # Skip the empty tile
            current_position = puzzle.index(tile)
            goal_position = goal.index(tile)

            # Calculate the row and column indices for the current and goal positions
            current_row, current_col = current_position // n, current_position % n
            goal_row, goal_col = goal_position // n, goal_position % n

            # Calculate the Manhattan distance for the current tile
            manhattan_distance = abs(current_row - goal_row) + abs(current_col - goal_col)
            total_manhattan_distance += manhattan_distance

    return total_manhattan_distance

def neighbors(puzzle):
    # Find the size of the puzzle (assuming it's a square)
    n = gWidth

    # Find the position of the empty space
    empty_index = puzzle.index("_")
    row, col = empty_index // n, empty_index % n

    # Define the possible moves (up, down, left, right)
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    neighbors = set()

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc

        # Check if the move is within bounds
        if 0 <= new_row < n and 0 <= new_col < n:
            new_index = new_row * n + new_col

            # Create a copy of the puzzle and swap the empty space with the neighbor
            neighbor_list = list(puzzle)
            neighbor_list[empty_index], neighbor_list[new_index] = neighbor_list[new_index], neighbor_list[empty_index]
            neighbor = "".join(neighbor_list)

            neighbors.add(neighbor)

    return neighbors
    
def count_inversions(state):
    inversions = 0
    state = state.replace("_", "")  # Remove the empty space from the state
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j]:
                inversions += 1
    return inversions

def is_solvable(start_state_str, goal_state_str):
   
    start_inversions = count_inversions(start_state_str)
    goal_inversions = count_inversions(goal_state_str)
   
    return (gWidth%2 == 1 and (start_inversions % 2) != (goal_inversions % 2)) or (gWidth%2 == 0 and ((start_inversions+rowOfSpace(start_state_str)) % 2) != ((goal_inversions+rowOfSpace(goal_state_str)) % 2))

def aStar(start, goal):
    if start == goal:
        return[start]
        
    if is_solvable(start, goal):
        return []

    open_set = Queue()
    closed_set = set()
    g_score = {start: 0}
    f_score = {start: h(start, goal)}
    parents = {}  # Store parents to reconstruct the path

    open_set.enqueue(start, f_score[start])

    while not open_set.is_empty():
        current_state = open_set.dequeue()

        if current_state == goal:
            path = []
            while current_state in parents:
                path.append(current_state)
                current_state = parents[current_state]
            path.reverse()
            return path

        closed_set.add(current_state)

        for neighbor in neighbors(current_state):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current_state] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor, goal)
                open_set.enqueue(neighbor, f_score[neighbor])
                parents[neighbor] = current_state

    return []
    
def compact(path):
    if len(path) <= 1:
        return "G"
    retStr = ""
    for i in range(1, len(path)):
        current_state = path[i - 1]
        next_state = path[i]

        empty_index = current_state.index("_")
        next_empty_index = next_state.index("_")

        if next_empty_index == empty_index - 1:
            retStr += "L"
        elif next_empty_index == empty_index + 1:
            retStr += "R"
        elif next_empty_index == empty_index - gWidth:
            retStr += "U"
        elif next_empty_index == empty_index + gWidth:
            retStr += "D"

    return retStr

puzzles = open(args[0]).read().split("\n")
print(f"{puzzles[0]} G")

for i in puzzles[1:]:
    v = [i] + aStar(i, puzzles[0])
    print(f"{i} {compact(v)}")


#Medha Pappula, 6, 2026