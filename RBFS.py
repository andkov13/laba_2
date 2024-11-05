import time
import random
# import psutil
# import threading
import os
import sys

# Обмеження рекурсивного виклику функцій(максимальна зафіксована кількість ітерацій ~ 20000)
recursion_limit = 20000
sys.setrecursionlimit(recursion_limit)

# Обмеження часу і пам'яті
# TIME_LIMIT_SEC = 10 * 60  # 10 хвилин
# MEMORY_LIMIT_MB = 512  # 512 Мб

# Завершення програми при перевищенні часу виконання
def terminate_program():
    print("Програма перевищила ліміт часу і буде завершена.")
    os._exit(1)

# # Завершення програми при перевищенні використання пам'яті
# def check_memory_limit():
#     process = psutil.Process(os.getpid())
#     while True:
#         mem_usage = process.memory_info().rss / (1024 * 1024)
#         if mem_usage > MEMORY_LIMIT_MB:
#             print("Програма перевищила ліміт пам'яті і буде завершена.")
#             os._exit(1)
#         time.sleep(1)

# # Запуск таймера
# timer = threading.Timer(TIME_LIMIT_SEC, terminate_program)
# timer.start()

# # Запуск моніторингу пам'яті
# memory_thread = threading.Thread(target=check_memory_limit)
# memory_thread.start()

# Цільовий стан задачі
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

# H1 - підрахунок фішок, які не на своїх місцях
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
    candidates = [best_neighbor]  # Список кандидатів із найкращим значенням (для рандомного вибору при рівності значень)
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
        # print("RBFS:")
        # print("Початковий стан:")
        start_state = generate_solvable_puzzle(goal_state, moves=30)
        # for row in start_state:
        #     print(row)

        start_time = time.time()

        result, depth = rbfs(start_state)

        end_time = time.time()
        elapsed_time = end_time - start_time  # Час виконання
        return result, depth, elapsed_time
        # if result == goal_state:
        #     print("Цільовий стан досягнуто.")
        #     print("Глибина:", depth)
        # else:
        #     print(f"За {recursion_limit-5} ітерацій рішення НЕ було знайдено")
        # print("Час роботи алгоритму:", elapsed_time, "секунд")
    except KeyboardInterrupt:
        print("Програма зупинена користувачем.")
    # finally:
    #     timer.cancel()  # Скасування таймера
