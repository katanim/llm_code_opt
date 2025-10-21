
#!/usr/bin/env python3

import argparse
import json
import os
from typing import List, Dict, Any, Optional

from tree_sitter import Language, Parser
from tree_sitter_languages import get_language

CPP_LANG_NAME = "cpp"

def extract_function_info(src: bytes, fn_node) -> Dict[str, Any]:
    for child in fn_node.children:
        if child.type == "function_declarator":
            function_declarator = src[child.start_byte:child.end_byte].decode("utf-8")
        elif child.type == "qualified_identifier":
            output_type = src[child.start_byte:child.end_byte].decode("utf-8")
        elif child.type == "compound_statement":
            body = src[child.start_byte:child.end_byte].decode("utf-8")
    return {
        "function_declarator": function_declarator,
        "body": body,
        "output type": output_type,
    }
        

def walk_functions(src: bytes, tree) -> List[Dict[str, Any]]:
    root = tree.root_node
    out = []

    def visit(node):
        # Collect out-of-class and in-class definitions alike
        if node.type == "function_definition":
            out.append(extract_function_info(src, node))
        # Recurse
        for ch in node.children:
            visit(ch)

    visit(root)
    return out

def main():
    ap = argparse.ArgumentParser(description="Extract C++ function definitions to JSON using tree-sitter.")
    ap.add_argument("cpp_file", help="Path to .cpp file")
    ap.add_argument("output_json", help="Path to write JSON")
    args = ap.parse_args()

    lang = get_language('cpp')
    parser = Parser()
    parser.set_language(lang)
    with open(args.cpp_file, "rb") as f:
        src = f.read()

    tree = parser.parse(src)
    funcs = walk_functions(src, tree)

    # Also include file-level metadata
    result = {
        "file": os.path.abspath(args.cpp_file),
        "num_functions": len(funcs),
        "functions": funcs,
    }

    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(funcs)} functions to {args.output_json}")

if __name__ == "__main__":
    main()
