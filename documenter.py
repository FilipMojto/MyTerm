from argparse import ArgumentParser

parser = ArgumentParser(description="Documenter Script")

parser.add_argument(
    "--input",
    type=str,
    required=False,
    default="data.json",
    help="Path to the input JSON file (default: data.json)",
)

