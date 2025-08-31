import sys
import json
import os
from pathlib import Path
from openai import OpenAI

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

def get_malfunction_from_openai(client, system_prompt, combination):
    """Get malfunction description from OpenAI for a function-keyword pair."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Describe a malfunction when {combination['function']} experiences condition: {combination['keyword']}"}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
            # temperature=0.7,
            # max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return None

def save_results(results, output_file):
    """Save results to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python hazop.py <functions_file> <keywords_file> <output_file>")
        sys.exit(1)

    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    functions_file = Path(sys.argv[1])
    keywords_file = Path(sys.argv[2])
    output_file = Path(sys.argv[3])

    # Initialize OpenAI client
    client = OpenAI()

    # Read input files
    functions = read_file_lines(functions_file)
    keywords = read_file_lines(keywords_file)

    # System prompt for OpenAI
    system_prompt = """You are a HAZOP analysis expert. For each function and keyword combination, 
    provide a brief, specific description of a potential malfunction. 
    The response shall be one sentence.

    Meaning of keywords:
    - No: Complete negation of the function.
    - More: Function occurs to a greater extent than intended.
    - Less: Function occurs to a lesser extent than intended.
    - As well as: An additional function occurs alongside the intended function.
    - Part of: Only a portion of the function occurs.
    - Reverse: The opposite of the intended function occurs.
    - Other than: A different function occurs instead of the intended one.
    - Early: The function occurs before it is supposed to.
    - Late: The function occurs after it is supposed to.
    - Before: The function occurs prior to a specified event or condition.
    - After: The function occurs following a specified event or condition.
    - Not: The function fails to occur when it should.    

    Example 1:
    - Function: The system shall measure temperature.
    - Keyword: Not
    - Malfunction: The system does not measure temperature.
    """

    # Generate combinations and get malfunctions
    results = []
    combinations = generate_hazop_combinations(functions, keywords)
    
    for combo in combinations:
        malfunction = get_malfunction_from_openai(client, system_prompt, combo)
        if malfunction:
            result = {
                "function": combo["function"],
                "keyword": combo["keyword"],
                "malfunction": malfunction
            }
            results.append(result)
            print(json.dumps(result))

    # Save all results to file
    save_results(results, output_file)
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()