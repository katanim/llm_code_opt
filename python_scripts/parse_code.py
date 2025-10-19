
#!/usr/bin/env python3

import argparse
import json
import os
from typing import List, Dict, Any, Optional

from tree_sitter import Language, Parser
from tree_sitter_languages import get_language

CPP_LANG_NAME = "cpp"

# --------- Helpers ---------
def load_language(so_path: Optional[str]) -> Language:
    so_path = (
        so_path
        or os.environ.get("TREE_SITTER_LANG_SO")
        or "build/my-languages.so"
    )
    if not os.path.exists(so_path):
        raise FileNotFoundError(
            f"Language .so not found at '{so_path}'. Pass --lang-so or set TREE_SITTER_LANG_SO."
        )
    return Language(so_path, CPP_LANG_NAME)

def node_text(src: bytes, node) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", errors="replace")

def find_child(node, types: List[str]):
    for ch in node.children:
        if ch.type in types:
            return ch
    return None

def find_descendant(node, types: List[str]):
    stack = [node]
    while stack:
        n = stack.pop()
        if n.type in types:
            return n
        stack.extend(n.children)
    return None

def collect_scope_names(src: bytes, node) -> List[str]:
    """Walk ancestors to collect enclosing namespaces and classes (outermost → innermost)."""
    names = []
    cur = node.parent
    while cur:
        if cur.type == "namespace_definition":
            ident = find_descendant(cur, ["identifier"])
            if ident:
                names.insert(0, node_text(src, ident).strip())
        elif cur.type in ("class_specifier", "struct_specifier"):
            ident = find_descendant(cur, ["type_identifier"])
            if ident:
                names.insert(0, node_text(src, ident).strip())
        cur = cur.parent
    return names

def extract_function_info(src: bytes, fn_node) -> Dict[str, Any]:
    # Declarator (contains name + parameter_list + qualifiers)
    declarator = find_descendant(fn_node, ["function_declarator"])
    if declarator is None:
        declarator = find_descendant(fn_node, ["declarator"])  # fallback

    # Function name (try qualified first, then identifier)
    name_node = find_descendant(declarator, [
        "qualified_identifier",
        "scoped_identifier",
        "field_identifier",
        "destructor_name",
        "operator_name",
        "identifier",
    ]) if declarator else None
    name_text = node_text(src, name_node).strip() if name_node else "<unknown>"

    # Parameter list
    params_node = find_descendant(declarator, ["parameter_list"]) if declarator else None
    params_text = node_text(src, params_node).strip() if params_node else "()"

    # Return / specifiers: everything before declarator
    if declarator:
        pre_text = src[fn_node.start_byte:declarator.start_byte].decode("utf-8", errors="replace").strip()
    else:
        pre_text = ""

    # Qualifiers after parameter list (e.g., const, noexcept, ref qualifiers)
    post_text = ""
    if declarator and params_node:
        post_text = src[params_node.end_byte:declarator.end_byte].decode("utf-8", errors="replace").strip()

    # Body (compound statement) text
    body_node = find_descendant(fn_node, ["compound_statement"])
    body_text = node_text(src, body_node).strip() if body_node else ""

    # Location
    loc = {
        "start_line": fn_node.start_point[0] + 1,
        "start_col": fn_node.start_point[1] + 1,
        "end_line": fn_node.end_point[0] + 1,
        "end_col": fn_node.end_point[1] + 1,
    }

    # Scope path (namespaces/classes)
    scope = collect_scope_names(src, fn_node)

    # Fully qualified (best-effort)
    fqn = "::".join(scope + [name_text]) if scope else name_text

    # Signature (best-effort)
    signature = f"{pre_text} {node_text(src, declarator).strip()}" if declarator else pre_text

    return {
        "name": name_text,
        "fully_qualified_name": fqn,
        "return_and_specifiers": pre_text,
        "parameter_list": params_text,
        "post_qualifiers": post_text,
        "signature": " ".join(signature.split()),
        "body": body_text,
        "location": loc,
        "scope": scope,
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
