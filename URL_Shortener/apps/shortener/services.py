ALPHABET = "23456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
BASE = len(ALPHABET)

def encode_base62(number: int) -> str:
    """Convert an integer ID to a short code."""
    
    if number == 0:
        return ALPHABET[0]

    encoded = []

    while number > 0:
        number, remainder = divmod(number, BASE)
        encoded.append(ALPHABET[remainder])

    encoded.reverse()
    return ''.join(encoded)

def decode_base62(code: str) -> int:
    """Convert a short code back to the original integer ID."""
    
    number = 0

    for char in code:
        number = number * BASE + ALPHABET.index(char)

    return number