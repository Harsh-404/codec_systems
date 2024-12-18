# test_performance.py
import unittest
import time
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from encoder import encode
from decoder import decode

class TestPerformance(unittest.TestCase):
    def test_large_data(self):
        with open("test_data.json", "r") as f:
            input_data = json.load(f)
            
        print(f"\nInput data type: {type(input_data)}")
        if isinstance(input_data, dict):
            print(f"Dictionary size: {len(input_data)}")
            print(f"Keys sample: {list(input_data.keys())[:5]}")
            
            def print_large_integers(data, path=""):
                if isinstance(data, dict):
                    for k, v in data.items():
                        new_path = f"{path}.{k}" if path else k
                        if isinstance(v, int) and v > 2**32-1:
                            print(f"Large integer at {new_path}: {v}")
                        print_large_integers(v, new_path)
                elif isinstance(data, list):
                    for i, v in enumerate(data):
                        new_path = f"{path}[{i}]"
                        if isinstance(v, int) and v > 2**32-1:
                            print(f"Large integer at {new_path}: {v}")
                        print_large_integers(v, new_path)
            
            print("\nScanning for large integers...")
            print_large_integers(input_data)
            
        start_time = time.time()
        try:
            encoded = encode(input_data, max_int=2**64-1, max_seq_len=1000000)
            print(f"Successfully encoded {len(encoded)} bytes")
            
            decoded = decode(encoded, max_int=2**64-1, max_seq_len=1000000)
            print(f"Successfully decoded back to original format")
            
            duration = time.time() - start_time
            print(f"Total time: {duration:.2f} seconds")

            self.assertEqual(decoded, input_data)
            self.assertTrue(duration < 5, "Performance test exceeded 5 seconds")
            
        except ValueError as e:
            print(f"\nError encoding/decoding data:")
            print(f"Error message: {str(e)}")
            print(f"Stack trace:")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    unittest.main()