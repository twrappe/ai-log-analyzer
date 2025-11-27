import json
from pathlib import Path
from jsonschema import validate, ValidationError

def validate_summary(summary, schema):
    try:
        validate(instance=summary, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)


def save_summary(summary, output_path: Path):
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)