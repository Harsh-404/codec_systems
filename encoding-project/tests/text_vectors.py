import pytest
from src.encoder import encode, EncodingError
import pytest
from src.encoder import encode

# Test Vector 1
INPUT_1 = {
    "null": None,
    "octets": bytes([1, 2, 3]),
    "integer": 12345
}
EXPECTED_1 = [
    0x03,                   # Dictionary with 3 items
    0x04, 0x6E, 0x75, 0x6C, 0x6C,         # "null"
    0x00,                   # Empty sequence
    0x06, 0x6F, 0x63, 0x74, 0x65, 0x74, 0x73,  # "octets"
    0x03, 0x01, 0x02, 0x03, # Byte sequence length 3
    0x07, 0x69, 0x6E, 0x74, 0x65, 0x67, 0x65, 0x72,  # "integer"
    0x39, 0x30             # 12345 in little-endian
]

# Test Vector 2
INPUT_2 = {
    "outer": {
        "inner": [1, 2, 3],
        "value": 42
    }
}
EXPECTED_2 = [
    0x01,                   # Dictionary with 1 item
    0x05, 0x6F, 0x75, 0x74, 0x65, 0x72,   # "outer"
    0x02,                   # Dictionary with 2 items
    0x05, 0x69, 0x6E, 0x6E, 0x65, 0x72,   # "inner"
    0x03, 0x01, 0x02, 0x03, # Array [1,2,3]
    0x05, 0x76, 0x61, 0x6C, 0x75, 0x65,   # "value"
    0x2A                    # 42
]

# Test Vector 3
INPUT_3 = 18446744073709551615  # 2^64 - 1
EXPECTED_3 = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def test_encode_null():
    result = encode(None)
    assert result == [0x00], "Null encoding failed"

def test_encode_basic_types():
    result = encode(INPUT_1)
    assert result == EXPECTED_1, "Basic types encoding failed"

def test_encode_nested_structure():
    result = encode(INPUT_2)
    assert result == EXPECTED_2, "Nested structure encoding failed"

def test_encode_large_integer():
    result = encode(INPUT_3)
    assert result == EXPECTED_3, "Large integer encoding failed"
    
def test_additional_encoding_scenarios():
    """Test additional encoding scenarios"""
    # Base64 encoded bytes
    base64_input = "SGVsbG8gV29ybGQ="  # "Hello World" in Base64
    expected_result = [len(b"Hello World")] + list(b"Hello World")
    result = encode(base64_input)
    assert result == expected_result, "Base64 decoding failed"

    # Unicode string
    unicode_input = "こんにちは"  # Japanese "Hello"
    expected_result = [len(unicode_input.encode('utf-8'))] + list(unicode_input.encode('utf-8'))

    result = encode(unicode_input)
    assert result == expected_result, "Unicode encoding failed"

# def test_error_handling():
#     """Test error handling for unsupported types"""
#     with pytest.raises(EncodingError):
#         encode(complex(1, 2))  # Unsupported type