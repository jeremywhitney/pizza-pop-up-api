import json
import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def validate_fixtures(fixture_dir: str) -> Tuple[bool, List[str]]:
    """
    Validate Django fixture files in a directory.

    Args:
        fixture_dir: Path to directory containing fixture files

    Returns:
        Tuple of (is_valid: bool, errors: List[str])
    """
    errors = []
    all_pks = defaultdict(set)  # model -> set of pks
    all_fks = defaultdict(set)  # model -> set of fks
    fk_references = defaultdict(set)  # model -> set of required fks

    # First pass: collect all PKs and FK references
    for filename in os.listdir(fixture_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(fixture_dir, filename)
        try:
            with open(filepath, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    errors.append(f"Invalid JSON in {filename}: {str(e)}")
                    continue

                if not isinstance(data, list):
                    errors.append(f"{filename}: Root element must be a list")
                    continue

                for item in data:
                    # Validate basic structure
                    if not all(k in item for k in ["model", "pk", "fields"]):
                        errors.append(
                            f"{filename}: Missing required keys (model, pk, fields)"
                        )
                        continue

                    model = item["model"]
                    pk = item["pk"]

                    # Check for duplicate PKs
                    if pk in all_pks[model]:
                        errors.append(
                            f"{filename}: Duplicate PK {pk} for model {model}"
                        )
                    all_pks[model].add(pk)

                    # Collect FK references
                    for field, value in item["fields"].items():
                        if isinstance(value, (int, str)) and field.endswith("_id"):
                            # This is likely a FK field
                            base_model = model.split(".")[0]
                            referenced_model = f"{base_model}.{field[:-3]}"
                            fk_references[referenced_model].add(value)
                        elif isinstance(value, list):
                            # This might be a M2M field
                            for v in value:
                                if isinstance(v, (int, str)):
                                    base_model = model.split(".")[0]
                                    referenced_model = f"{base_model}.{field}"
                                    fk_references[referenced_model].add(v)

        except Exception as e:
            errors.append(f"Error processing {filename}: {str(e)}")

    # Second pass: validate FK references
    for model, refs in fk_references.items():
        for ref in refs:
            if ref not in all_pks[model]:
                errors.append(f"Missing FK reference: {model} with pk={ref}")

    # Return results
    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    """
    Main function to run the validator.
    """
    fixture_dir = "pizzaapi/fixtures"

    print("Validating fixtures...")
    is_valid, errors = validate_fixtures(fixture_dir)

    if is_valid:
        print("✅ All fixtures are valid!")
    else:
        print("❌ Found the following errors:")
        for error in errors:
            print(f"  • {error}")


if __name__ == "__main__":
    main()
