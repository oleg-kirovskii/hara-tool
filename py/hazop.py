import sys
import os
from pathlib import Path
from hara_tool.input_handler import read_file_lines, generate_hazop_combinations
from hara_tool.openai_client import HazopAIClient
from hara_tool.output_handler import save_results, print_result

def main():
    if len(sys.argv) != 4:
        print("Usage: python hazop.py <functions_file> <keywords_file> <output_file>")
        sys.exit(1)

    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    functions_file = Path(sys.argv[1])
    keywords_file = Path(sys.argv[2])
    output_file = Path(sys.argv[3])

    # Initialize components
    ai_client = HazopAIClient()

    # Read input files
    functions = read_file_lines(functions_file)
    keywords = read_file_lines(keywords_file)

    # Generate combinations and get malfunctions
    results = []
    combinations = generate_hazop_combinations(functions, keywords)
    
    for combo in combinations:
        malfunction = ai_client.get_malfunction(combo)
        if malfunction:
            result = {
                "function": combo["function"],
                "keyword": combo["keyword"],
                "malfunction": malfunction
            }
            results.append(result)
            print_result(result)

    # Save all results to file
    save_results(results, output_file)
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()