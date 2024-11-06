import time
import random
import os
import sys

recursion_limit = 20000
sys.setrecursionlimit(recursion_limit)

def terminate_program():
    print("Програма перевищила ліміт часу і буде завершена.")
    os._exit(1)

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Пошук порожньої клітинки
def get_empty_tile_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Пошук нащадків вузла
def get_neighbors(state):
    neighbors = []
    x, y = get_empty_tile_position(state)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

# підрахунок фішок, які не на своїх місцях
def h1(state):
    mismatch_count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j] and state[i][j] != 0:
                mismatch_count += 1
    return mismatch_count

# Вибір найкращого збігу
def get_best_neighbor(neighbors):
    best_neighbor = neighbors[0]
    best_score = h1(best_neighbor)
    candidates = [best_neighbor] 
    for n in neighbors[1:]:
        score = h1(n)
        if score < best_score:
            best_score = score
            candidates = [n]
        elif score == best_score:
            candidates.append(n)
    return random.choice(candidates)

# Рекурсивний пошук за першим найкращим збігом
def rbfs(current_state, previous_state=None, depth=0):
    if current_state == goal_state:
        return current_state, depth
    elif depth > recursion_limit-5:
        return current_state, depth
    depth += 1
    neighbors = get_neighbors(current_state)

    # Видалення попереднього стану із сусідів, щоб уникнути зациклення
    if previous_state in neighbors:
        neighbors.remove(previous_state)

    best_neighbor = get_best_neighbor(neighbors)

    # Рекурсивний виклик з оновленими параметрами
    previous_state = current_state
    return rbfs(best_neighbor, previous_state, depth)

# Генерація початкового стану шляхом тасування кінцевого стану
def generate_solvable_puzzle(goal_state, moves=10):
    state = [row[:] for row in goal_state]
    for _ in range(moves):
        neighbors = get_neighbors(state)
        state = random.choice(neighbors)
    return state

def attempt():
    try:
        start_state = generate_solvable_puzzle(goal_state, moves=30)
        start_mem = start_state.copy()

        start_time = time.time()

        result, depth = rbfs(start_state)

        end_time = time.time()
        elapsed_time = end_time - start_time  
        return result, start_mem, depth, elapsed_time
    except KeyboardInterrupt:
        print("Програма зупинена користувачем.")

