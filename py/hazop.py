import sys
import json
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

def main():
    if len(sys.argv) != 3:
        print("Usage: python hazop.py <functions_file> <keywords_file>")
        sys.exit(1)

    functions_file = Path(sys.argv[1])
    keywords_file = Path(sys.argv[2])

    functions = read_file_lines(functions_file)
    keywords = read_file_lines(keywords_file)

    combinations = generate_hazop_combinations(functions, keywords)
    
    # Print each combination as JSON
    for combo in combinations:
        print(json.dumps(combo))

if __name__ == "__main__":
    main()