import random
import time
import tracemalloc


def fitness(board):
    """Higher is better (max = no conflicts)"""
    n = len(board)
    non_attacking = 0

    max_pairs = (n * (n - 1)) // 2

    for i in range(n):
        for j in range(i + 1, n):

            if board[i] != board[j] and abs(i - j) != abs(board[i] - board[j]):
                non_attacking += 1

    return non_attacking


def create_population(size, n):
    return [[random.randint(0, n - 1) for _ in range(n)] for _ in range(size)]


def crossover(parent1, parent2):
    point = random.randint(0, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child


def mutate(board, mutation_rate=0.1):
    if random.random() < mutation_rate:
        row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board) - 1)
        board[row] = col
    return board


def genetic_algorithm(n, population_size=100, generations=500, time_limit=5):

    population = create_population(population_size, n)

    start_time = time.time()

    best_solution = None
    best_fitness = -1

    for _ in range(generations):

        if time.time() - start_time > time_limit:
            return best_solution, False, True

        population = sorted(population, key=fitness, reverse=True)

        if fitness(population[0]) == (n * (n - 1)) // 2:
            return population[0], True, False

        new_population = population[:10]  # elitism

        while len(new_population) < population_size:

            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])

            child = crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

        if fitness(population[0]) > best_fitness:
            best_solution = population[0]
            best_fitness = fitness(population[0])

    return best_solution, False, False


def run_experiment(n):

    tracemalloc.start()
    start = time.time()

    solution, solved, timeout = genetic_algorithm(n)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\nN =", n)
    print("Solved:", solved)
    print("Solution:", solution)
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


main()