# plotter.py
# Module for plotting (Task 3)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 17.05.2025

import matplotlib.pyplot as plt

class Plotter:
    """Handles plotting and saving of series vs math.log."""
    def __init__(self, x, series, analytic):
        self.x = x
        self.series = series
        self.analytic = analytic

    def _draw(self):
        plt.plot(self.x, self.series, marker='o', linestyle='', label="Series Approx")
        plt.plot(self.x, self.analytic, linestyle='--', label="math.log")
        plt.axhline(0, color='gray', linestyle='-')
        plt.axvline(0, color='gray', linestyle='-')
        plt.title("ln(1+x): Series vs Analytic")
        plt.xlabel("x")
        plt.ylabel("F(x)")
        plt.legend()
        plt.grid(True)
        errors = [abs(a - b) for a, b in zip(self.series, self.analytic)]
        idx = errors.index(max(errors))
        plt.annotate(
            f"Max error at x={self.x[idx]:.2f}",
            xy=(self.x[idx], self.series[idx]),
            xytext=(self.x[idx] + 0.05, self.series[idx] - 0.1),
            arrowprops=dict(arrowstyle='->', color='black')
        )

    def plot(self):
        """Display the plot."""
        plt.figure()
        self._draw()
        plt.show()

    def save(self, filename):
        """Save the plot to a PNG file."""
        plt.figure()
        self._draw()
        plt.savefig(filename, dpi=300)
        plt.close()
