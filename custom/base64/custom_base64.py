import array
import base64
import string
import sys
import time
from collections.abc import Iterable

if sys.byteorder not in ('little', 'big'):
    raise RuntimeError('only little or big endian are supported')


_base64_alphabet: str = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
_base64_alphabet_ordinals: list[int] = [ord(ch) for ch in _base64_alphabet]

_base64url_alphabet: str = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_"
_base64url_alphabet_ordinals: list[int] = [ord(ch) for ch in _base64url_alphabet]


def _encode_impl(data: bytes, alphabet: list[int]) -> bytes:
    """operates on 192-bit (24 byte) chunks (3x 64-bit ints)"""
    mv = memoryview(data)
    tail_length: int = len(mv) % 24
    head_length: int = len(mv) - tail_length
    arr_64b = array.array('Q')
    arr_64b.frombytes(mv[:head_length])

    if sys.byteorder != 'big':
        arr_64b.byteswap()

    base64_bytes: bytearray = bytearray((head_length + tail_length + 2) // 3 * 4)

    for iteration, i in enumerate(range(0, head_length // 8, 3)):
        q1_64b, q2_64b, q3_64b = arr_64b[i], arr_64b[i+1], arr_64b[i+2]

        # extract 4*8=32 6-bit sequences (s1_6b - s32_6b) from the 24 bytes
        # iterate q1
        bitshift = 64
        for inner_iteration in range(0, 10):
            bitshift -= 6
            s_6b = (q1_64b >> bitshift) & 0x3F
            base64_bytes[iteration * 32 + inner_iteration] = alphabet[s_6b]

        # deal with the q1-q2 mix
        s11_6b = ((q1_64b & 0xF) << 2) | (q2_64b >> 62)  # q1[4..1] | q2[64..63]
        base64_bytes[iteration * 32 + 10] = alphabet[s11_6b]

        # iterate q2
        bitshift = 62
        for inner_iteration in range(11, 21):
            bitshift -= 6
            s_6b = (q2_64b >> bitshift) & 0x3F
            base64_bytes[iteration * 32 + inner_iteration] = alphabet[s_6b]

        # deal with the q2-q3 mix
        s22_6b = ((q2_64b & 0x3) << 4) | (q3_64b >> 60)  # q2[2..1] | q3[64..61]
        base64_bytes[iteration * 32 + 21] = alphabet[s22_6b]

        # iterate q3
        bitshift = 60
        for inner_iteration in range(22, 32):
            bitshift -= 6
            s_6b = (q3_64b >> bitshift) & 0x3F
            base64_bytes[iteration * 32 + inner_iteration] = alphabet[s_6b]

    if tail_length > 0:
        pad_length: int = (24 - tail_length)
        padded_tail_bytes = data[head_length:] + b'\x00' * pad_length
        # assert len(padded_tail_bytes) == 24
        encoded_tail = _encode_impl(padded_tail_bytes, alphabet)
        # assert len(encoded_tail) == 32

        if pad_length >= 3:
            cutoff: int = pad_length // 3 * 4
            encoded_tail = encoded_tail[:-cutoff]
            pad_length = pad_length % 3

        if pad_length > 0:
            encoded_tail = encoded_tail[:-pad_length] + b'=' * pad_length

        base64_bytes[-len(encoded_tail):] = encoded_tail

    return base64_bytes


def _decode_chunk(chunk: bytes, alphabet_index_lookup: dict[int, int]) -> bytes:
    """
    A chunk is a 4 byte long base64 sequence that gets turned into it's respective 1, 2, or 3 byte long decoded sequence

    :param chunk: 4-byte long sequence
    :return: 1, 2, or 3 byte long decoded sequence
    """
    # separate the chunk into its 4 base64 chars and convert the base64 chars to their respective 6-bit sequence
    # check the _encode_chunk function to see how these are being extracted the other way around
    s1, s2, s3, s4 = (alphabet_index_lookup[char] for char in chunk)

    # reconstruct the 3 bytes from the 4 6-bit sequences
    first_byte: int = (s1 << 2) | (s2 >> 4)  # s1 | upper 2 bits from s2
    second_byte: int = ((s2 & 0xF) << 4) | (s3 >> 2)  # lower 4 bits from s2 | upper 4 bits from s3
    third_byte: int = ((s3 & 0b11) << 6) | s4  # lower 2 bits from s3 | s4

    original_bytes: list[int] = [first_byte, second_byte, third_byte]

    # trim zero bytes
    if padding := chunk.count(b'='):  # [[unlikely]]
        original_bytes = original_bytes[:-padding]

    return bytes(original_bytes)


def _data_to_chunks(data: bytes, chunk_size: int) -> Iterable[bytes]:
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def _decode_impl(base64_encoding: bytes, alphabet: str) -> bytes:
    alphabet_index_lookup: dict[int, int] = {ord(char): index for index, char in enumerate(alphabet)}
    alphabet_index_lookup[ord('=')] = 0

    return b''.join(_decode_chunk(chunk, alphabet_index_lookup) for chunk in _data_to_chunks(base64_encoding, 4))


def encode(data: bytes) -> bytes:
    return _encode_impl(data, _base64_alphabet_ordinals)


def decode(base64_encoding: bytes) -> bytes:
    return _decode_impl(base64_encoding, _base64_alphabet)


def encode_url(data: bytes) -> bytes:
    return _encode_impl(data, _base64url_alphabet_ordinals)


def decode_url(base64_encoding: bytes) -> bytes:
    return _decode_impl(base64_encoding, _base64url_alphabet)


with open("Docker Desktop Installer.exe", "rb") as datafile:
    plaintext: bytes = datafile.read()


if __name__ == '__main__':
    MY_ENCODE = True

    start = time.time()
    if MY_ENCODE:
        encoded_plaintext: bytes = encode(plaintext)
    else:
        encoded_plaintext: bytes = base64.encodebytes(plaintext)

    print(f"{len(encoded_plaintext):,} bytes")
    print(f"Took {time.time() - start:.2f} seconds")