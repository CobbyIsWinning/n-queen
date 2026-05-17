"""
Run experiments from each solver and plot the results.
Generates: time vs N and memory vs N for each algorithm and a solved-rate bar chart.

Usage:
    python plot_results.py

This script imports `run_experiment` from each solver module so the solvers must not execute on import
(we added guards to their main()).

"""

import matplotlib.pyplot as plt
import numpy as np

from dfs import run_experiment as dfs_run
from genetic_algorithim import run_experiment as ga_run
from hill_climbing import run_experiment as hc_run
from simulated_annealing import run_experiment as sa_run

ALGORITHMS = {
    "DFS": dfs_run,
    "Genetic": ga_run,
    "HillClimbing": hc_run,
    "SimulatedAnnealing": sa_run,
}

TEST_VALUES = [10, 30, 50, 100, 200, 500]


def collect_results(test_values=TEST_VALUES):
    results = {name: [] for name in ALGORITHMS}

    for n in test_values:
        print(f"\nRunning experiments for N={n}")
        for name, fn in ALGORITHMS.items():
            print(f" Running {name}...", end=" ")
            try:
                r = fn(n)
            except Exception as e:
                print(f"Error: {e}")
                r = {"N": n, "Solved": False, "Time": None, "MemoryKB": None, "Timeout": True}

            results[name].append(r)
            print("done")

    return results


def plot_time_memory(results, test_values=TEST_VALUES, out_prefix="nqueen"):
    # use a builtin style to avoid dependency on seaborn
    plt.style.use('ggplot')

    # Time plot
    plt.figure(figsize=(10, 6))
    for name, res in results.items():
        times = [r['Time'] if r['Time'] is not None else np.nan for r in res]
        plt.plot(test_values, times, marker='o', label=name)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('N (log scale)')
    plt.ylabel('Time (s, log scale)')
    plt.title('Solver Time vs N')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_time.png")
    print(f"Saved {out_prefix}_time.png")

    # Memory plot
    plt.figure(figsize=(10, 6))
    for name, res in results.items():
        mems = [r['MemoryKB'] if r['MemoryKB'] is not None else np.nan for r in res]
        plt.plot(test_values, mems, marker='o', label=name)

    plt.xscale('log')
    plt.xlabel('N (log scale)')
    plt.ylabel('Memory (KB)')
    plt.title('Solver Peak Memory vs N')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_memory.png")
    print(f"Saved {out_prefix}_memory.png")


def plot_solved_rate(results, test_values=TEST_VALUES, out_prefix="nqueen"):
    # For each N, compute solved counts per algorithm
    solved_counts = {name: [1 if r.get('Solved') else 0 for r in res] for name, res in results.items()}

    x = np.arange(len(test_values))  # label positions
    width = 0.2

    plt.figure(figsize=(12, 6))

    for i, (name, counts) in enumerate(solved_counts.items()):
        plt.bar(x + i * width, counts, width=width, label=name)

    plt.xticks(x + width * (len(solved_counts) - 1) / 2, test_values)
    plt.xlabel('N')
    plt.ylabel('Solved (1=yes, 0=no)')
    plt.title('Solved status per algorithm and N')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_solved.png")
    print(f"Saved {out_prefix}_solved.png")


if __name__ == '__main__':
    results = collect_results()
    plot_time_memory(results)
    plot_solved_rate(results)

    print('\nAll plots generated.')
