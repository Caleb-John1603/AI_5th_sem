import copy

# Define the target configuration (0 represents the empty tile)
GOAL_STATE = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5)
)

def find_blank(state):
    """Find the (row, col) coordinates of the blank space (0)."""
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_neighbors(state):
    """Generate all valid next states by sliding adjacent tiles."""
    neighbors = []
    r, c = find_blank(state)
    
    # Possible moves: (row_change, col_change, action_name)
    moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]
    
    for dr, dc, move_name in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            # Convert tuple of tuples to list of lists to allow item assignment
            new_board = [list(row) for row in state]
            # Swap the blank tile with the target tile
            new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
            # Convert back to immutable tuple of tuples (hashable & safe for path tracking)
            neighbors.append((tuple(tuple(row) for row in new_board), move_name))
            
    return neighbors

def depth_limited_dfs(state, goal, depth, path, actions):
    """Performs a depth-limited DFS tracking the current path."""
    if state == goal:
        return actions
    
    if depth <= 0:
        return None
    
    # Track the state in the current recursion branch to avoid cyclic loops
    path.add(state)
    
    for neighbor, move in get_neighbors(state):
        if neighbor not in path:
            result = depth_limited_dfs(neighbor, goal, depth - 1, path, actions + [move])
            if result is not None:
                return result
                
    # Backtrack: remove from branch path tracking
    path.remove(state)
    return None

def id_dfs(initial_state, goal_state):
    """Iterative Deepening DFS wrapper."""
    depth = 0
    while True:
        # path set tracks ancestors to prevent looping back up the current branch
        path = set() 
        result = depth_limited_dfs(initial_state, goal_state, depth, path, [])
        if result is not None:
            return result, depth
        depth += 1

def print_board(state):
    """Helper function to cleanly display the grid layout."""
    for row in state:
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()

# --- Example Execution ---
if __name__ == "__main__":
    # 0 represents the empty space
    # This specific setup requires a short sequence of moves to find the goal easily
    initial = (
        (2, 8, 3),
        (1, 0, 4),
        (7, 6, 5)
    )
    
    print("Initial State:")
    print_board(initial)
    
    print("Searching for solution using IDDFS...")
    moves_sequence, execution_depth = id_dfs(initial, GOAL_STATE)
    
    print(f"Solution found at depth {execution_depth}!")
    print(f"Moves Sequence: {moves_sequence}")
