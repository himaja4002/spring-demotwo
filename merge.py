def merge_json(original, filters):
    # Load the original JSON structure
    original_data = json.loads(original["config"])
    
    # Extract the encodings from the original JSON structure
    encodings = original_data[0]["encodings"]

    # Iterate over each filter in filters.json
    for filter_item in filters:
        name = filter_item["name"]
        rule = filter_item["rule"]

        # Search for the corresponding dragId in the original.json for the filter name
        matching_encodings = [e for e in encodings["dimensions"] if e["name"] == name]

        if matching_encodings:
            encoding = matching_encodings[0]
            encoding["rule"] = rule
            # Add this encoding to the filters list in the original JSON
            if "filters" not in encodings:
                encodings["filters"] = []
            encodings["filters"].append(encoding)

    original["config"] = json.dumps(original_data)
    return original

# Read the original.json and filters.json directly from the directory
with open("original.json", "r") as f:
    original = json.load(f)

with open("filters.json", "r") as f:
    filters = json.load(f)

# Combine the original and filters JSON
result = merge_json(original, filters)

# Write the result to updated.json
with open("updated.json", "w") as f:
    json.dump(result, f)

