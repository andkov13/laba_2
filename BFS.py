import time
import random
import psutil
import threading
import os

# Обмеження часу і пам'яті
TIME_LIMIT_SEC = 10 * 60  # 10 хвилин
MEMORY_LIMIT_MB = 512  # 512 Мб

# Завершення програми при перевищенні часу виконання
def terminate_program():
    print("Програма перевищила ліміт часу і буде завершена.")
    os._exit(1)

# Завершення програми при перевищенні використання пам'яті
# def check_memory_limit():
#     process = psutil.Process(os.getpid())
#     while True:
#         mem_usage = process.memory_info().rss / (1024 * 1024)
#         if mem_usage > MEMORY_LIMIT_MB:
#             print("Програма перевищила ліміт пам'яті і буде завершена.")
#             os._exit(1)
#         time.sleep(1)

# Запуск таймера
timer = threading.Timer(TIME_LIMIT_SEC, terminate_program)
timer.start()

# # Запуск моніторингу пам'яті
# memory_thread = threading.Thread(target=check_memory_limit)
# memory_thread.start()

# цільовий стан задачі
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

# Пошук в ширину
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
        # print("BFS:")
        # print("Початковий стан:")
        start_state = generate_solvable_puzzle(goal_state, moves = 30)
        # for row in start_state:
        #     print(row)
        start_time = time.time()
        result, depth = bfs(start_state)
        end_time = time.time()
        elapsed_time = end_time - start_time  # Час виконання

        # if result:
        #     print("Цільовий стан досягнуто.")
        #     print("Глибина:", depth)
        # else:
        #     print("Рішення не знайдено.")
        # print("Час роботи алгоритму:", elapsed_time, "секунд")

        return (result, depth, elapsed_time)
    except KeyboardInterrupt:
        print("Програма зупинена користувачем.")
    finally:
        timer.cancel()  # Скасування таймера


