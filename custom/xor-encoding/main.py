import random

def human_optimized_encode_xor(data: bytes) -> tuple[bytes, int]:
    """Picks the best possible encoding, in terms of readability of the encoding for a human (no real purpose in that)"""
    def human_score(ciphertext: bytes) -> int:
        return sum(chr(byte).isascii() and chr(byte).isprintable() for byte in ciphertext)

    best_encodings: list[tuple[bytes, int]] = []
    best_score: int = -1
    for key in range(0xFF):
        encoded_message: bytes = _encode_xor_impl(data, key)
        curr_score: int = human_score(encoded_message)

        if curr_score > best_score:
            best_score = curr_score
            best_encodings.clear()

        if curr_score >= best_score:
            best_encodings.append((encoded_message, key))

    return random.choice(best_encodings)


def _encode_xor_impl(plaintext: bytes, key: int) -> bytes:
    cipher_bytes: list[int] = []
    for character in plaintext:
        key ^= character
        cipher_bytes.append(key)

    return bytes(cipher_bytes)


def encode_xor(data: bytes) -> tuple[bytes, int]:
    key: int = random.randint(0, 0xFF)

    return _encode_xor_impl(data, key), key


def decode_xor(ciphertext: bytes, key: int) -> str:
    plain_bytes: list[int] = []
    cipher_byte: int

    for cipher_byte in ciphertext:
        plain_bytes.append(key ^ cipher_byte)
        key = cipher_byte

    return bytes(plain_bytes).decode()