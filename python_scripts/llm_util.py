from google import genai
import json


def test_api_call(client):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain how AI works in a few words",
    )
    print(response.text)

def print_function_body(client, input_json_path):
    with open(input_json_path, 'r') as f:
        data = json.load(f)
    funcs = data.get("functions", [])
    for i, fn in enumerate(funcs, 1):
        decl = fn.get("function_declarator", f"function_{i}")
        body = fn.get("body", "")
        # Ask Gemini to format the code
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= "Format this C++ code with proper syntax:\n" + body
        )
        print("Function Body:")
        print(response.text)

def naive_optimization(client, input_json_path):
    with open(input_json_path, 'r') as f:
        data = json.load(f)
    funcs = data.get("functions", [])
    for i, fn in enumerate(funcs, 1):
        decl = fn.get("function_declarator", f"function_{i}")
        body = fn.get("body", "")
        # Ask Gemini to optimize the code
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= "Optimize this C++ code for performance. Provide only the complete, optimized C++ code block.:\n" + body
        )
    return response.text

def guided_optimization(client, input_json_path, tile_size: int = 8, unroll_factor: int = 4):
    with open(input_json_path, 'r') as f:
        data = json.load(f)
    funcs = data.get("functions", [])
    for i, fn in enumerate(funcs, 1):
        decl = fn.get("function_declarator", f"function_{i}")
        body = fn.get("body", "")
        # Ask Gemini to optimize the code for a specific goal
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= f"Refactor the following C++ code to apply tiling and unrolling with a tile size of {tile_size} and unrolling factor of {unroll_factor}. The transformed code must be functionally equivalent to the original and pass all original test cases. Provide only the complete, transformed C++ code block.\n" + body
        )
    return response.text

def provide_test_cases(client, input_json_path):
    with open(input_json_path, 'r') as f:
        data = json.load(f)
    funcs = data.get("functions", [])
    for i, fn in enumerate(funcs, 1):
        decl = fn.get("function_declarator", f"function_{i}")
        body = fn.get("body", "")
        # Ask Gemini to provide test cases
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= "Provide unit test cases in C++ for the following function. Ensure the tests cover edge cases and typical usage scenarios. Provide only the complete C++ code block for the test cases.\n" + body
        )
    return response.text


def main():
    client = genai.Client()
    response = print_function_body(client, '/home/amin/projects/llm_code_opt/out.json')
    print(response)

if __name__ == "__main__":
    main()