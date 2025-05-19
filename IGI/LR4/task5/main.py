# Main module for exploring NumPy matrix tasks and user interaction (Task 5)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025


from array_creation import create_random_matrix
from indexing import split_even_odd_index_elements
from stats_ops import (
    min_row_sum, compute_mean, compute_median,
    compute_variance, compute_std, compute_corrcoef
)


def get_positive_int(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val > 0:
                return val
        except ValueError:
            pass
        print("Please enter a positive integer.")


def main():
    print("NumPy Matrix Exploration Task")
    while True:
        n = get_positive_int("Enter number of rows (n): ")
        m = get_positive_int("Enter number of columns (m): ")

        A = create_random_matrix(n, m, low=0, high=100)
        print("Matrix A:")
        print(A)

        # a) array ops demo
        print("Mean:", compute_mean(A))
        print("Median:", compute_median(A))
        print("Variance:", compute_variance(A))
        print("Std Dev:", compute_std(A))

        # min row sum
        print("Min row sum:", min_row_sum(A))

        # even/odd index correlation
        even, odd = split_even_odd_index_elements(A)
        corr = compute_corrcoef(even, odd)
        print(f"Corrcoef between even/odd indexed elements: {corr:.4f}")

        again = input("Run again? (y/n): ").strip().lower()
        if again != 'y':
            break


if __name__ == '__main__':
    main()
