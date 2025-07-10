import json
import plistlib

def parse_config(filepath):
    try:
        if filepath.endswith('.json'):
            with open(filepath, 'r') as f:
                return json.load(f)
        elif filepath.endswith('.plist'):
            with open(filepath, 'rb') as f:
                return plistlib.load(f)
        else:
            return {"error": "Unsupported file type"}
    except Exception as e:
        return {"error": str(e)}
