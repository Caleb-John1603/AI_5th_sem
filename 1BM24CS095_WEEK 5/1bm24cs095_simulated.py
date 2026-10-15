import random
import math

def get_cost(state):
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                attacks += 1
            elif abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def get_neighbor(state):
    neighbor = list(state)
    row = random.randint(0, 7)
    col = random.randint(0, 7)
    while col == state[row]:
        col = random.randint(0, 7)
    neighbor[row] = col
    return neighbor

def simulated_annealing(initial_state):
    current = list(initial_state)
    current_cost = get_cost(current)
    
    T = 100.0
    cooling_rate = 0.95
    
    while T > 0.001 and current_cost > 0:
        next_state = get_neighbor(current)
        next_cost = get_cost(next_state)
        delta_E = current_cost - next_cost
        
        if delta_E > 0:
            current = next_state
            current_cost = next_cost
        else:
            p = math.exp(delta_E / T)
            if random.random() < p:
                current = next_state
                current_cost = next_cost
                
        T *= cooling_rate
        
    return current, current_cost

def display_board(state):
    for row in range(8):
        line = ""
        for col in range(8):
            if state[row] == col:
                line += " Q "
            else:
                line += " . "
        print(line)


custom_initial_state = [0, 1, 2, 3, 4, 5, 6, 7] 

print("Initial State Array:", custom_initial_state)
solution, final_cost = simulated_annealing(custom_initial_state)

print(f"\nFinal State Array: {solution} (Conflicts: {final_cost})")
print("\nFinal Chessboard Grid Visual:")
display_board(solution)
