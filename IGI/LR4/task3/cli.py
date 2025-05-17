# Module for CLI interface (Task 3)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 17.05.2025

from ln_series import LnSeriesCalculator
from plotter import Plotter

def get_float_input(prompt, cond, err):
    """Prompt until valid float satisfying cond."""
    while True:
        try:
            val = float(input(prompt))
            if not cond(val):
                print(err)
                continue
            return val
        except ValueError:
            print("Invalid number, try again.")

def run():
    print("=== ln(1+x) Series Analyzer ===")
    while True:
        x_start = get_float_input("Start x (> -1): ", lambda v: v > -1, "Must be > -1")
        x_end   = get_float_input("End x (<= 1): ", lambda v: v <= 1, "Must be <= 1")
        if x_end <= x_start:
            print("End must be > start")
            continue
        step = get_float_input("Step (> 0): ", lambda v: v > 0, "Must be >0")
        eps  = get_float_input("Epsilon (> 0): ", lambda v: v > 0, "Must be >0")
        calc = LnSeriesCalculator(eps)
        try:
            calc.compute_sequence(x_start, x_end, step)
        except ValueError as e:
            print(f"Error: {e}")
            continue
        print("\nx\tSeries F(x)\tn\tMath F(x)")
        for x_val, f_val, n_val, m_val in zip(calc.x_values, calc.f_values, calc.n_values, calc.math_f_values):
            print(f"{x_val:.2f}\t{f_val:.6f}\t{n_val}\t{m_val:.6f}")
        stats_data = {
            'mean': calc.mean(calc.f_values),
            'median': calc.median(calc.f_values),
            'mode': calc.mode(calc.f_values),
            'variance': calc.variance(calc.f_values),
            'std_dev': calc.std_dev(calc.f_values)
        }
        print("\nStatistics:")
        for key, value in stats_data.items():
            print(f"{key}: {value}")
        plotter = Plotter(calc.x_values, calc.f_values, calc.math_f_values)
        plotter.plot()
        fname = input("Filename to save plot (or empty to skip): ")
        if fname:
            plotter.save(fname)
            print(f"Saved to {fname}")
        if input("Run again? (y/n): ").strip().lower() != 'y':
            break