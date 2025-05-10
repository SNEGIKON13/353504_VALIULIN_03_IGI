# Module for file operations (Task 2)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 24.10.2023

import os

def read_file(path):
    """
    Read the content of a text file.
    Args:
        path: Path to the file
    Returns:
        Content of the file or None if an error occurs
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_results(results, output_path):
    """
    Write results to a text file.
    Args:
        results: List of strings to write
        output_path: Path to the output file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in results:
                f.write(line + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")