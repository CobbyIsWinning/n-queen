import time
import tracemalloc
import signal

# Timeout settings because DFS can take a long time for larger N
TIME_LIMIT = 5  # seconds per experiment


class TimeoutException(Exception):
    pass


def handler(signum, frame):
    raise TimeoutException()


signal.signal(signal.SIGALRM, handler)


# N-Queens Solver using DFS
def is_safe(board, row, col):
    for i in range(row):

        if board[i] == col:
            return False

        if abs(row - i) == abs(col - board[i]):
            return False

    return True


def solve_nqueens(board, row):
    n = len(board)

    if row == n:
        return True

    for col in range(n):

        if is_safe(board, row, col):

            board[row] = col

            if solve_nqueens(board, row + 1):
                return True

            board[row] = -1

    return False


# function to run a single experiment for a given N
def run_experiment(n):

    board = [-1] * n

    tracemalloc.start()
    start = time.time()

    result = False
    timeout = False

    try:
        signal.alarm(TIME_LIMIT)  # start countdown
        result = solve_nqueens(board, 0)
        signal.alarm(0)  # cancel alarm if finished

    except TimeoutException:
        timeout = True
        result = False

    end = time.time()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    duration = end - start

    print("\nN =", n)
    print("Solved:", result)
    print("Time (s):", round(duration, 4))
    print("Memory (KB):", round(peak / 1024, 2))
    print("Timeout:", timeout)

    return {
        "N": n,
        "Solved": result,
        "Time": duration,
        "MemoryKB": peak / 1024,
        "Timeout": timeout
    }

# main function to run experiments for different N values
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