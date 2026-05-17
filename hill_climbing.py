import random
import time
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


def hill_climbing(n, max_iterations=10000, time_limit=5):

    board = [random.randint(0, n - 1) for _ in range(n)]

    start_time = time.time()

    for _ in range(max_iterations):

        if time.time() - start_time > time_limit:
            return board, False, True

        current_conflicts = calculate_conflicts(board)

        if current_conflicts == 0:
            return board, True, False

        best_board = board[:]
        best_conflicts = current_conflicts

        for row in range(n):

            if time.time() - start_time > time_limit:
                return board, False, True

            original_col = board[row]

            for col in range(n):

                if time.time() - start_time > time_limit:
                    return board, False, True

                if col == original_col:
                    continue

                board[row] = col

                new_conflicts = calculate_conflicts(board)

                if new_conflicts < best_conflicts:
                    best_conflicts = new_conflicts
                    best_board = board[:]

            board[row] = original_col

        if best_conflicts == current_conflicts:
            return board, False, False

        board = best_board

    return board, False, True


def run_experiment(n):

    tracemalloc.start()

    start = time.time()

    solution, solved, timeout = hill_climbing(n)

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