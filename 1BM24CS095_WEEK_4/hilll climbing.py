import heapq

def get_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                conflicts += 1
            elif abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        original_row = state[col]
        for row in range(n):
            if row != original_row:
                neighbor = list(state)
                neighbor[col] = row
                neighbors.append(tuple(neighbor))
    return neighbors

def solve_4_queens(initial_state):
    start = tuple(initial_state)
    frontier = []
    heapq.heappush(frontier, (get_conflicts(start), start))
    visited = set()
    iteration = 1

    while frontier:
        cost, current = heapq.heappop(frontier)
        
        if current in visited:
            continue
            
        visited.add(current)
        print(f"Iteration {iteration}: Current State = {list(current)}, Conflicts = {cost}")
        
        if cost == 0:
            print(f"\n Success! Solution found at iteration {iteration}: {list(current)}")
            return list(current)
            
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                neighbor_cost = get_conflicts(neighbor)
                heapq.heappush(frontier, (neighbor_cost, neighbor))
                
        iteration += 1
        
    print("\n No solution found.")
    return None

if __name__ == "__main__":
    my_start_state = [3, 1, 2, 0]
    solve_4_queens(my_start_state)
