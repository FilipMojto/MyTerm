import json
from argparse import ArgumentParser
from typing import List, Dict, Any  
from .config import INPUT_FILE_PATH as CFG_INPUT_FILE_PATH 

def load_terms(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("terms", [])

def load_areas(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    areas = set()
    for term in data.get("terms", []):
        areas.add(term["area"])
    return list(areas)

def match_partial(value: str, query: str) -> bool:
    """Case-insensitive partial match."""
    return query.lower() in value.lower()


def filter_terms(
    terms: List[Dict[str, Any]],
    id_: int = None,
    term: str = None,
    definition: str = None,
    area: str = None,
    example: int = None,
    see_also: int = None
) -> List[Dict[str, Any]]:
    results = []

    for t in terms:
        if id_ is not None and t["id"] != id_:
            continue

        if term and not match_partial(t["term"], term):
            continue

        if definition:
            matching_defs = [
                d for d in t["definitions"]
                if match_partial(d.get("definition", ""), definition)
            ]

            if not matching_defs:
                continue  # nothing matched — skip whole term

            # keep only matching definitions
            t = t.copy()
            t["definitions"] = matching_defs
                    
        if area and not match_partial(t["area"], area):
            continue

        if example is not None and example not in t.get("examples", []):
            continue

        if see_also is not None and see_also not in t.get("see_also", []):
            continue
        
        results.append(t)
            
    return results

DEF_INPUT_FILE_PATH = CFG_INPUT_FILE_PATH

def main():
    parser = ArgumentParser(description="JSON terminology search tool")

    parser.add_argument("--input", type=str, default=DEF_INPUT_FILE_PATH,
                        help="Path to the input terminology JSON file")

    # Search parameters
    parser.add_argument("--id", type=int, help="Filter by ID")
    parser.add_argument("--term", type=str, help="Partial match in term name")
    parser.add_argument("--definition", type=str, help="Partial match in definition")
    parser.add_argument("--area", type=str, help="Filter by area (partial match ok)")
    parser.add_argument("--example", type=int, help="Filter by example reference")
    parser.add_argument("--see-also", type=int, help="Filter by see-also reference")
    parser.add_argument("--areas", action="store_true",
                        help="List all unique areas in the terminology")
    parser.add_argument("--full-print", action="store_true",
                        help="Print full entries instead of summaries")
    

    args = parser.parse_args()

    terms = load_terms(args.input)

    areas = load_areas(args.input) if args.areas else None

    filtered = filter_terms(
        terms,
        id_=args.id,
        term=args.term,
        definition=args.definition,
        area=args.area,
        example=args.example,
        see_also=args.see_also
    )

    if not filtered:
        print("No results found.")
        return

    for t in filtered:
        print("-" * 60)
        print(f"ID: {t['id']}")
        print(f"Term: {t['term']}")
        print(f"Area: {t['area']}")
        print("Definitions:")
        for defn in t["definitions"]:
            print(f"  - {defn.get('definition')} (Source: {defn.get('source')})")
        print(f"Examples: {t.get('examples', [])}")
        print(f"See also: {t.get('see_also', [])}")
        if args.full_print:
            print(f"Notes: {t.get('notes', [])}")
    
    if areas is not None:
        print("\nUnique Areas:")
        for area in areas:
            print(f"- {area}")


if __name__ == "__main__":
    main()