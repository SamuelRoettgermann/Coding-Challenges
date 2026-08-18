"""A file for stuff that was abandoned during the development of the custom_base64.py,
just because I didn't want to throw it all away.
Also because especially the early versions are much more educational than the newer, more optimized ones"""

import string
from collections.abc import Iterable

_base64_alphabet: str = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
_base64url_alphabet: str = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_"

# version 1
def _encode_chunk(chunk: bytes, alphabet: bytes) -> bytes:
    """
    A chunk is a 1-3 byte long sequence that gets turned into it's respective 4 byte long base64 encoding.

    :param chunk: 1-3 byte long sequence
    :return: base 64 encoded 4 byte chunk
    """
    # pad chunk to be 3-byte long - only happens for the last chunk
    padding: int = 3 - len(chunk)
    if padding:  # [[unlikely]]
        chunk += bytes(padding)

    # implicit conversion to int
    b1, b2, b3 = chunk

    # extract 4 6-bit sequences from the bytes, named here s1, s2, s3, s4
    s1 = b1 >> 2  # b1[8..3]
    s2 = ((b1 & 0b11) << 4) | (b2 >> 4)  # b1[2..1] | b2[8..5]
    s3 = ((b2 & 0b1111) << 2) | (b3 >> 6)  # b2[4..1] | b3[8..7]
    s4 = b3 & 0x3F  # b3[6..1]

    encoding: bytes = bytes((
        alphabet[s1],
        alphabet[s2],
        alphabet[s3],
        alphabet[s4],
    ))

    # adjust for possible previous padding:
    if padding:  # [[unlikely]]
        encoding = encoding[:-padding] + (b'=' * padding)

    return encoding


def _data_to_chunks(data: bytes, chunk_size: int) -> Iterable[bytes]:
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def _encode_impl(data: bytes, alphabet: str) -> bytes:
    alphabet_bytes = bytes(alphabet, encoding="ascii")

    return b''.join(_encode_chunk(chunk, alphabet_bytes) for chunk in _data_to_chunks(data, 3))

def encode(data: bytes) -> bytes:
    return _encode_impl(data, _base64_alphabet)


# version 2 was cameron's version (can be found on Discord)

# version 3
def _encode_impl(data: bytes, alphabet: list[int]) -> bytes:
    mv = memoryview(data)
    tail_length: int = len(mv) % 3
    head_length: int = len(mv) - tail_length

    base64_bytes: bytearray = bytearray(head_length * 4 // 3 + (tail_length > 0) * 4)

    for iteration, i in enumerate(range(0, head_length, 3)):
        b1, b2, b3 = mv[i], mv[i + 1], mv[i + 2]

        # extract 4 6-bit sequences (s1_6b - s4_6b) from the bytes b1 - b3
        s1_6b = b1 >> 2  # b1[8..3]
        s2_6b = ((b1 & 0b11) << 4) | (b2 >> 4)  # b1[2..1] | b2[8..5]
        s3_6b = ((b2 & 0b1111) << 2) | (b3 >> 6)  # b2[4..1] | b3[8..7]
        s4_6b = b3 & 0x3F  # b3[6..1]

        base64_bytes[iteration * 4 + 0] = alphabet[s1_6b]
        base64_bytes[iteration * 4 + 1] = alphabet[s2_6b]
        base64_bytes[iteration * 4 + 2] = alphabet[s3_6b]
        base64_bytes[iteration * 4 + 3] = alphabet[s4_6b]

    if tail_length > 0:
        pad_length: int = 3 - tail_length
        padded_tail_bytes = data[head_length:] + b'\x00' * pad_length
        # assert len(padded_tail_bytes) == 3
        encoded_tail = _encode_impl(padded_tail_bytes, alphabet)
        # assert len(encoded_tail) == 4

        if pad_length > 0:
            encoded_tail = encoded_tail[:-pad_length] + b'=' * pad_length
            # assert len(encoded_tail) == 4

        base64_bytes[-4:] = encoded_tail

    return base64_bytes