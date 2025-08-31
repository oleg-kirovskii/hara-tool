import json

def save_results(results, output_file):
    """Save results to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

def print_result(result):
    """Print a single result to console."""
    print(json.dumps(result))