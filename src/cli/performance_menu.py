"""Run or view benchmark reports without changing interactive structures."""

from src.cli.application import Application
from src.cli.navigation import run_menu
from src.performance.benchmark import run_benchmark
from src.performance.result import BenchmarkResult, format_results, save_results


def run_performance(app: Application) -> BenchmarkResult:
    print(f"Benchmarking the original {len(app.records)} loaded students.")
    result = run_benchmark(app.records)
    destination = save_results(result, app.results_path)
    print(format_results(result), end="")
    print(f"Results saved to: {destination}")
    return result


def view_results(app: Application) -> None:
    try:
        report = app.results_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("No saved benchmark results yet. Run the benchmark first.")
        return
    print(report, end="" if report.endswith("\n") else "\n")


def performance_menu(app: Application) -> None:
    run_menu("Performance Comparison", {
        "1": ("Run Hash vs. Linear Search Benchmark", lambda: run_performance(app)),
        "2": ("View Latest Results", lambda: view_results(app)),
    })
