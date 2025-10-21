import json
from jsonschema import validate, ValidationError
from pathlib import Path

# -------------------------
# Helper functions
# -------------------------

def load_json(file_path):
    """Load a JSON file and return the data"""
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_logs(log_file):
    """Parse raw log file into structured events (dummy example)"""
    events = []
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                events.append({"raw": line})
    return events

def summarize_logs(events, blueprint):
    """
    Summarize events using blueprint instructions.
    For now, this is a placeholder that structures logs.
    """
    summary = {"log_summary": []}
    for event in events:
        # Apply blueprint rules (simplified example)
        summary_item = {
            "message": event["raw"],
            "category": blueprint.get("default_category", "general")
        }
        summary["log_summary"].append(summary_item)
    return summary

def validate_summary(summary, schema):
    """Validate the summarized JSON against the schema"""
    try:
        validate(instance=summary, schema=schema)
        print("✅ Summary is valid according to schema.")
    except ValidationError as e:
        print("❌ Validation Error:", e)

# -------------------------
# Main workflow
# -------------------------

def main():
    # Paths
    schema_folder = "schema\\"
    logs_folder = "examples\\sample_logs\\"
    schema_path = Path(schema_folder + "schema.json")
    blueprint_path = Path(schema_folder + "blueprint.json")
    log_file_path = Path(logs_folder + "Windows_2k.log")  # change for other OS logs
    output_path = Path(schema_folder + "summary.json")

    # Load schema and blueprint
    schema = load_json(schema_path)
    blueprint = load_json(blueprint_path)

    # Parse logs
    events = parse_logs(log_file_path)
    print(f"Parsed {len(events)} events from {log_file_path}")

    # Summarize logs using blueprint
    summary = summarize_logs(events, blueprint)

    # Validate summary against schema
    validate_summary(summary, schema)

    # Save summary
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {output_path}")

# Entry point
if __name__ == "__main__":
    main()
