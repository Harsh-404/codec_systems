
def decode(encoded_bytes, max_int=2**64-1, max_seq_len=1000000):
    if not isinstance(encoded_bytes, bytes):
        raise ValueError("Input must be bytes")
        
    pos = 0
    
    def decode_integer(pos):
        value = 0
        shift = 0
        
        while pos < len(encoded_bytes):
            byte = encoded_bytes[pos]
            pos += 1
            
            value |= (byte & 0x7F) << shift
            if value > max_int:
                raise ValueError(f"Integer overflow: {value}")
                
            if not (byte & 0x80):  
                break
                
            shift += 7
            if shift >= 64: 
                raise ValueError("Integer too large")
                
        return value, pos


    def decode_string(pos):
        length, pos = decode_integer(pos)
        if length > max_seq_len:
            raise ValueError(f"String length exceeds maximum: {length}")
        if pos + length > len(encoded_bytes):
            raise ValueError("Invalid string length")
        try:
            string = encoded_bytes[pos:pos+length].decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("Invalid UTF-8 sequence")
        return string, pos + length

    def decode_sequence(pos):
        length, pos = decode_integer(pos)
        if length > max_seq_len:
            raise ValueError(f"Sequence length exceeds maximum: {length}")
            
        sequence = []
        for _ in range(length):
            value, pos = decode_value(pos)
            sequence.append(value)
        return sequence, pos

    def decode_dict(pos):
        size, pos = decode_integer(pos)
        if size > max_seq_len:
            raise ValueError(f"Dictionary size exceeds maximum: {size}")
            
        result = {}
        for _ in range(size):
            # Decode key length and key
            key_len, pos = decode_integer(pos)
            if key_len > max_seq_len:
                raise ValueError(f"Key length exceeds maximum: {key_len}")
            if pos + key_len > len(encoded_bytes):
                raise ValueError("Invalid key length")
            try:
                key = encoded_bytes[pos:pos+key_len].decode('utf-8')
            except UnicodeDecodeError:
                raise ValueError("Invalid UTF-8 sequence in key")
            pos += key_len
            
            # Decode value
            value, pos = decode_value(pos)
            result[key] = value
            
        return result, pos

    def decode_value(pos):
        if pos >= len(encoded_bytes):
            raise ValueError("Unexpected end of input")
            
        marker = encoded_bytes[pos]
        pos += 1
        
        if marker == 0x00:
            return None, pos
        elif marker == 0x01:
            return decode_sequence(pos)
        elif marker == 0x02:
            return decode_dict(pos)
        elif marker == 0x03:
            return decode_integer(pos)
        elif marker == 0x04:
            return decode_string(pos)
        else:
            raise ValueError(f"Invalid marker: {marker}")

    result, pos = decode_value(0)
    if pos != len(encoded_bytes):
        raise ValueError("Extra data after end of value")
    return result