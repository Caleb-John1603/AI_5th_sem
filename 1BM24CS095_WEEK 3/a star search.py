import heapq

GOAL_STATE = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5)
)

class PuzzleNode:
    def __init__(self, state, g_cost, parent=None, move="Start"):
        self.state = state
        self.g_cost = g_cost
        self.parent = parent
        self.move = move
        self.h_cost = self.calculate_misplaced_tiles()
        self.f_cost = self.g_cost + self.h_cost

    def calculate_misplaced_tiles(self):
        misplaced = 0
        for r in range(3):
            for c in range(3):
                val = self.state[r][c]
                if val != 0 and val != GOAL_STATE[r][c]:
                    misplaced += 1
        return misplaced

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def get_blank_position(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_neighbors(node):
    neighbors = []
    r, c = get_blank_position(node.state)
    
    moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
    
    for dr, dc, direction in moves:
        new_r, new_c = r + dr, c + dc
        
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_state = [list(row) for row in node.state]
            new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
            
            final_state = tuple(tuple(row) for row in new_state)
            neighbors.append(PuzzleNode(final_state, node.g_cost + 1, node, direction))
            
    return neighbors

def solve_a_star(start_state):
    start_node = PuzzleNode(start_state, 0)
    
    open_set = []
    heapq.heappush(open_set, start_node)
    
    visited = set()
    
    while open_set:
        current_node = heapq.heappop(open_set)
        
        if current_node.state == GOAL_STATE:
            return reconstruct_path(current_node)
            
        visited.add(current_node.state)
        
        for neighbor in get_neighbors(current_node):
            if neighbor.state in visited:
                continue
            
            heapq.heappush(open_set, neighbor)
            
    return None

def reconstruct_path(node):
    path = []
    current = node
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]


if __name__ == "__main__":
    initial_puzzle = (
        (2, 8, 3),
        (1, 6, 4),
        (7, 0, 5)
    )
    
    print("Initial State:")
    for r in initial_puzzle: 
        print(f"  {r[0]} {r[1]} {r[2]}")
    print("\nSolving...")
    
    solution = solve_a_star(initial_puzzle)
    
    if solution:
        print(f"Goal reached in {len(solution) - 1} moves!\n")
        for step in solution:
            print(f"Move: {step.move} (g={step.g_cost}, h={step.h_cost}, f={step.f_cost})")
            for r in step.state:
                print(f"  {r[0]} {r[1]} {r[2]}")
            print()
    else:
        print("No solution could be found.")
