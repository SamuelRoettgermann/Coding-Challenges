import enum
import time
import base64
import timeit

import custom_base64

class Mode(enum.Enum):
    ENCODE_ONLY = enum.auto()
    ENCODE_AND_DECODE = enum.auto()
    VERIFY_INTEGRITY_ONLY = enum.auto()
    NOTHING = enum.auto()

N = 4
CHANGE: str = "Switched back to Windows to avoid further indirections"
MODE = Mode.VERIFY_INTEGRITY_ONLY

if MODE in (Mode.ENCODE_ONLY, Mode.ENCODE_AND_DECODE, Mode.VERIFY_INTEGRITY_ONLY):
    print("Starting integrity check...")
    for text in (b"a", b"ab", b"abc", b"abcd", b"This is a longer test sentence.",
                 b'Very very long sentence hihuha, I am a monkey in a banana jungle :monkey: @grave'):
        mine_encoded = custom_base64.encode(text)
        official_encoded = base64.encodebytes(text)
        official_encoded = b''.join(official_encoded.splitlines())

        if mine_encoded != official_encoded:
            print(f"FAIL Encode for {text}:\n\t{mine_encoded = }\n\t{official_encoded = }")

        mine_decoded = custom_base64.decode(mine_encoded)
        official_decoded = base64.decodebytes(official_encoded)

        if not mine_decoded == text == official_decoded:
            print(f"FAIL Decode for {text}:\n\t{mine_decoded = }\n\t{official_decoded = }")

    print("Finished integrity check.")

    if MODE == Mode.VERIFY_INTEGRITY_ONLY:
        exit(0)


with open("Docker Desktop Installer.exe", "rb") as datafile:
    plaintext: bytes = datafile.read()

with open("log-benchmarks.txt", "a+") as file:
    def log_helper(operation: str, func, *args) -> bytes:
        func_result: bytes = b""

        total_operation_time: float = timeit.timeit(func, *args, number=N)
        print(f"\t{operation} took {total_operation_time} seconds")

        file.write(f"{operation}: {total_operation_time / N:.3f} s/iteration"
                   f" ({(filesize * N // (2 ** 20)) / total_operation_time:.2f} MiB/s)\n")

        return func_result


    file.write("=======================\n\n")
    file.write(f"{CHANGE}:\n\n")
    filesize: int = len(plaintext)
    file.write(f"N={N}, {filesize = :,} Byte\n")

    start_time: float = time.time()

    if MODE in (Mode.ENCODE_ONLY, Mode.ENCODE_AND_DECODE):
        log_helper("encode", custom_base64.encode, plaintext)
        log_helper("encode_official", base64.encodebytes, plaintext)


        file.write(f"encoding completed in {time.time() - start_time:.2f} seconds\n\n")

        file.flush()
        print("encoding finished")

    if MODE == Mode.ENCODE_AND_DECODE:
        start_decode_time: float = time.time()
        encoded_text = base64.encodebytes(plaintext)

        log_helper("decode", custom_base64.decode, encoded_text)
        log_helper("decode_official", base64.b64decode, encoded_text)

        file.write(f"decoding completed in {time.time() - start_decode_time:.2f} seconds\n")
        print("decoding finished")

    file.write(f"\nTest completed in {time.time() - start_time:.2f} seconds\n\n")
    print("Test finished")