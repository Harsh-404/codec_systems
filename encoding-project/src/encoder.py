
def encode(data, max_int=2**64-1, max_seq_len=1000000):
    result = []
    
    def encode_integer(n):
        if not isinstance(n, int):
            raise TypeError(f"Value must be an integer, got {type(n)}")
        if n < 0:
            raise ValueError("Integer must be non-negative")
        if n > max_int:
            raise ValueError("Integer too large")
            
        bytes_list = []
        while n > 0:
            byte = n & 0x7F
            n >>= 7
            if n > 0:
                byte |= 0x80
            bytes_list.append(byte)
        
        if not bytes_list:
            bytes_list.append(0)
            
        return bytes_list

    def encode_sequence(seq):
        if len(seq) > max_seq_len:
            raise ValueError(f"Sequence length exceeds maximum of {max_seq_len}")
            
        result.extend(encode_integer(len(seq)))
        
        if isinstance(seq, bytes):
            result.extend(seq)
        elif isinstance(seq, list):
            for item in seq:
                encode_value(item)

    def encode_string(s):
        if not isinstance(s, str):
            raise ValueError("Value must be a string")
        str_bytes = s.encode('utf-8')
        if len(str_bytes) > max_seq_len:
            raise ValueError(f"String length exceeds maximum of {max_seq_len}")
        result.extend(encode_integer(len(str_bytes)))
        result.extend(str_bytes)
        
    def encode_dict(d):
        if not isinstance(d, dict):
            raise TypeError("Value must be a dictionary")
            
        if len(d) > max_seq_len:
            raise ValueError(f"Dictionary size exceeds maximum of {max_seq_len}")
            
        result.extend(encode_integer(len(d)))
        
        for key in sorted(d.keys()):
            if not isinstance(key, str):
                raise TypeError("Dictionary keys must be strings")
                
            key_bytes = key.encode('utf-8')
            result.extend(encode_integer(len(key_bytes)))
            result.extend(key_bytes)
            encode_value(d[key])

    def encode_value(value):
        if value is None:
            result.append(0x00)
        elif isinstance(value, (bytes, list)):
            result.append(0x01)
            encode_sequence(value)
        elif isinstance(value, dict):
            result.append(0x02)
            encode_dict(value)
        elif isinstance(value, int):
            result.append(0x03)
            result.extend(encode_integer(value))
        elif isinstance(value, str):
            result.append(0x04)
            encode_string(value)
        else:
            raise TypeError(f"Unsupported type: {type(value).__name__}")

    encode_value(data)
    return bytes(result)