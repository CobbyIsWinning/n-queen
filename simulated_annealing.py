import random
import time
import math
import tracemalloc


def calculate_conflicts(board):
    conflicts = 0
    n = len(board)

    for i in range(n):
        for j in range(i + 1, n):

            if board[i] == board[j]:
                conflicts += 1

            if abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1

    return conflicts


def simulated_annealing(n, time_limit=5):

    board = [random.randint(0, n - 1) for _ in range(n)]

    temperature = n * n
    cooling_rate = 0.99

    start_time = time.time()

    current_conflicts = calculate_conflicts(board)

    while temperature > 1:

        if time.time() - start_time > time_limit:
            return board, False, True

        if current_conflicts == 0:
            return board, True, False

        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)

        new_board = board[:]
        new_board[row] = col

        new_conflicts = calculate_conflicts(new_board)

        delta = new_conflicts - current_conflicts

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            board = new_board
            current_conflicts = new_conflicts

        temperature *= cooling_rate

    return board, current_conflicts == 0, False


def run_experiment(n):

    tracemalloc.start()
    start = time.time()

    solution, solved, timeout = simulated_annealing(n)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\nN =", n)
    print("Solved:", solved)
    print("Time (s):", round(end - start, 4))
    print("Memory (KB):", round(peak / 1024, 2))
    print("Timeout:", timeout)

    return {
        "N": n,
        "Solved": solved,
        "Time": end - start,
        "MemoryKB": peak / 1024,
        "Timeout": timeout
    }


def main():

    test_values = [10, 30, 50, 100, 200, 500]

    results = []

    for n in test_values:
        results.append(run_experiment(n))

    print("\nSUMMARY")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()