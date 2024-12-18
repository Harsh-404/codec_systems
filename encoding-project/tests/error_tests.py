# tests/error_tests.py
import unittest
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from encoder import encode
from decoder import decode

class TestErrorHandling(unittest.TestCase):
    def test_invalid_input_types(self):
        # Test set
        with self.assertRaisesRegex(TypeError, "Unsupported type: set"):
            encode(set([1, 2, 3]))
            
        # Test custom object
        class CustomObject:
            pass
        with self.assertRaisesRegex(TypeError, "Unsupported type: CustomObject"):
            encode(CustomObject())

    def test_integer_overflow(self):
        # Test positive overflow
        with self.assertRaisesRegex(ValueError, "Integer too large"):
            encode(2**64)
            
        # Test negative numbers
        with self.assertRaisesRegex(ValueError, "Integer must be non-negative"):
            encode(-1)

    def test_sequence_length_limit(self):
        # Use a more reasonable size for testing
        max_seq_len = 1000000
        large_sequence = [0] * (max_seq_len + 1)  # Just over the limit
        with self.assertRaisesRegex(ValueError, "Sequence length exceeds maximum"):
            encode(large_sequence, max_seq_len=max_seq_len)

    def test_invalid_dictionary_keys(self):
        # Test non-string keys
        invalid_dict = {42: "value"}
        with self.assertRaisesRegex(TypeError, "Dictionary keys must be strings"):
            encode(invalid_dict)
            
        # Test None as key
        invalid_dict = {None: "value"}
        with self.assertRaisesRegex(TypeError, "Dictionary keys must be strings"):
            encode(invalid_dict)

    def test_decode_invalid_data(self):
        # Test invalid marker
        with self.assertRaisesRegex(ValueError, "Invalid marker"):
            decode(b'\xFF')
            
        # Test truncated data
        with self.assertRaisesRegex(ValueError, "Unexpected end of input"):
            decode(b'\x02\x01')  # Dictionary marker with incomplete data
            
        # Test invalid UTF-8
        with self.assertRaisesRegex(ValueError, "Invalid UTF-8 sequence"):
            decode(b'\x04\x01\xFF')  # String marker with invalid UTF-8

if __name__ == "__main__":
    unittest.main()