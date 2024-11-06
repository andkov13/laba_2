import time
import random
import threading
import os

TIME_LIMIT_SEC = 10 * 60  
MEMORY_LIMIT_MB = 512  

def terminate_program():
    print("Програма перевищила ліміт часу і буде завершена.")
    os._exit(1)

timer = threading.Timer(TIME_LIMIT_SEC, terminate_program)
timer.start()

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

# Пошук вширину
def bfs(start_state):
    visited = []
    queue = []
    visited.append(start_state)
    queue.append((start_state, 0))

    while queue:
        current_state, depth = queue.pop(0)

        if current_state == goal_state:
            return current_state, depth
        
        neighbors = get_neighbors(current_state)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append((neighbor, depth + 1))

        if depth > 16:
            break

    return None, depth

# Генерація початкового стану шляхом тасування кінцевого стану
def generate_solvable_puzzle(goal_state, moves=10):
    state = [row[:] for row in goal_state]
    for _ in range(moves):
        neighbors = get_neighbors(state)
        state = random.choice(neighbors)
    return state


def attempt():
    try:
        start_state = generate_solvable_puzzle(goal_state, moves = 30)
        start_mem = start_state.copy()
        start_time = time.time()
        result, depth = bfs(start_state)
        end_time = time.time()
        elapsed_time = end_time - start_time  

        return result, start_mem, depth, elapsed_time
    except KeyboardInterrupt:
        print("Програма зупинена користувачем.")
    finally:
        timer.cancel() 


