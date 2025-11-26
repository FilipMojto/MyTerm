import json
from pathlib import Path
from argparse import ArgumentParser

from .config import INPUT_FILE_PATH as cfg_INPUT_FILE_PATH

# Define the required structure for each term entry
REQUIRED_KEYS = {
    "id": None,               # normally int, but keep None if missing
    "term": "",
    "definitions": [],        # list of {definition, source}
    "examples": [],           # list of example IDs
    "see_also": [],           # list of related term IDs
    "notes": [],              # NEW field
    "area": ""
}

def normalize_term_entry(entry: dict) -> dict:
    """
    Ensures that each entry contains all required keys.
    Missing keys are inserted with default values.
    Extra keys are preserved.
    """
    normalized = entry.copy()

    for key, default in REQUIRED_KEYS.items():
        if key not in normalized:
            normalized[key] = default

    return normalized

def normalize_json(input_path: str):
    """
    Loads the JSON file, normalizes it, and writes the result
    to a new file named <original>_normalized.json.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Load JSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "terms" not in data or not isinstance(data["terms"], list):
        raise ValueError("JSON must contain a top-level 'terms' key containing a list.")

    # Normalize all terms
    normalized_terms = [
        normalize_term_entry(entry)
        for entry in data["terms"]
    ]

    # Prepare output file path
    output_path = input_path.with_name(input_path.stem + "_normalized.json")

    # Write normalized JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"terms": normalized_terms}, f, indent=4, ensure_ascii=False)

    print(f"Normalization complete. Wrote output to:\n{output_path}")

DEF_INPUT_FILE_PATH = cfg_INPUT_FILE_PATH

if __name__ == "__main__":
    arg_parser = ArgumentParser(description="Normalize JSON schema for term entries.")
    arg_parser.add_argument("input_file", type=str, default=DEF_INPUT_FILE_PATH, nargs="?",
                            help="Path to the input JSON file to normalize.")
    args = arg_parser.parse_args()
    # Example usage: change the file name here
    # normalize_json("terms.json")
    normalize_json(args.input_file)