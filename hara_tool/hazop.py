import sys
from pathlib import Path

def read_file_lines(file_path):
    """Read lines from a file and return non-empty stripped lines."""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

def generate_hazop_combinations(functions, keywords):
    """Generate all combinations of functions and HAZOP keywords as dictionaries."""
    combinations = []
    for func in functions:
        for keyword in keywords:
            combinations.append({
                "function": func,
                "keyword": keyword
            })
    return combinations