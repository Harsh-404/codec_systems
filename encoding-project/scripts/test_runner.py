import argparse
import json
import time
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from encoder import encode
from decoder import decode

def main():
    # Argument Parsing
    parser = argparse.ArgumentParser(description="Test runner for encoder decoder")
    parser.add_argument("--input", required=True, help="encoding-project test_data.json")
    parser.add_argument("--output", required=True, help="encoding-project results.json")
    parser.add_argument("--performance", action="store_true", help="Enable performance measurement")
    args = parser.parse_args()

    # Load Input Data
    with open(args.input, "r") as f:
        input_data = json.load(f)

    result = {"result": "success", "time": None, "outputSize": None, "inputSize": None}

    try:
        # Measure encoding/decoding time if performance flag is set
        start_time = time.time() if args.performance else None

        # Encode Data
        encoded_data = encode(input_data)
        result["outputSize"] = len(encoded_data)

        # Decode Data
        decoded_data = decode(encoded_data)

        # Measure time
        if args.performance:
            result["time"] = int((time.time() - start_time) * 1000)

        # Verify correctness
        if decoded_data != input_data:
            result["result"] = "failed"
        else:
            result["result"] = "success"

    except Exception as e:
        result["result"] = "failed"
        result["error"] = str(e)

    # Save Results
    with open(args.output, "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()
