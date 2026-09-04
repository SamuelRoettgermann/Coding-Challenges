import sys
import math
import time

sys.set_int_max_str_digits(0)

GREEN_COLOR = "\033[38;2;38;207;10m"
RED = "\033[38;2;250;3;3m"
WHITE = "\033[38;2;255;255;255m"
PI_COLOR = "\033[38;2;172;156;140m"
SUCCESS_COLOR = "\033[38;2;31;255;28m"
WARN_COLOR = "\033[38;2;253;247;0m"
ERROR_COLOR = "\033[38;2;253;0;0m"
RESET = "\033[0m"


def generate_pi_optimized(n_digits):
    """Calculates Pi using Binary Splitting Chudnovsky"""
    if n_digits <= 0:
        return ""
    if n_digits == 1:
        return "3"

    N = n_digits // 14 + 1

    lookup_table = [(1, 1, 13591409)] + \
                   [(
                       pab := ((6 * a - 5) * (2 * a - 1) * (6 * a - 1)),
                       a * a * a * 10939058860032000,
                       pab * (13591409 + 545140134 * a) * (-1) ** (a & 1)
                   ) for a in range(1, N)]

    def bs(a: int = 0, b: int = N):
        if b == a + 1:
            return lookup_table[a]

        m = (a + b) // 2
        Pam, Qam, Tam = bs(a, m)
        Pmb, Qmb, Tmb = bs(m, b)

        # Pab = Pam * Pmb
        # Qab = Qam * Qmb
        # Tab = Qmb * Tam + Pam * Tmb
        return Pam * Pmb, Qam * Qmb, Qmb * Tam + Pam * Tmb

    _, Q, T = bs()

    extra_digits = 10
    D = n_digits + extra_digits

    sqrt_term = math.isqrt(10005 * 10 ** (2 * D))
    pi_scaled = (426880 * Q * sqrt_term) // T

    return f"3.{str(pi_scaled)[1:n_digits]}"


def generate_pi(n_digits):
    """Calculates Pi using a blazing fast Binary Splitting Chudnovsky algorithm."""
    if n_digits <= 0:
        return ""
    if n_digits == 1:
        return "3"

    N = n_digits // 14 + 1

    def bs(a, b):
        # print(f"bs({a}, {b})")
        if b - a == 1:
            if a == 0:
                Pab = Qab = 1
            else:
                Pab = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
                Qab = (a ** 3) * 10939058860032000  # (640320^3) / 24
            Tab = Pab * (13591409 + 545140134 * a)
            if a & 1:
                Tab = -Tab

            # print(f"\t({Pab}, {Qab}, {Tab})")
        else:
            m = (a + b) // 2
            Pam, Qam, Tam = bs(a, m)
            Pmb, Qmb, Tmb = bs(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb

        return Pab, Qab, Tab

    P, Q, T = bs(0, N)
    # print(f"\n{P = }, {Q = }, {T = }")

    extra_digits = 10
    D = n_digits + extra_digits

    sqrt_term = math.isqrt(10005 * 10 ** (2 * D))
    pi_scaled = (426880 * Q * sqrt_term) // T

    pi_str = str(pi_scaled)
    result = pi_str[0] + "." + pi_str[1:]

    return result[:n_digits + 1]


class DigitCreationException(Exception):
    def __init__(self, message):
        super().__init__(message)


if __name__ == "__main__":
    actual_digits = 3000000

    print(f"\n{WHITE}Generating digits...{RESET}\n")
    start = time.perf_counter()
    pi_result = generate_pi(actual_digits)
    end = time.perf_counter()
    # print(f"{PI_COLOR}{pi_result}{RESET}\n")
    print(f"Calculation took {end - start} seconds.")

    print(f"\n{WHITE}Generating digits (optimized)...{RESET}\n")
    start_optimized = time.perf_counter()
    pi_result_optimized = generate_pi_optimized(actual_digits)
    end_optimized = time.perf_counter()
    # print(f"{PI_COLOR}{pi_result_optimized}{RESET}\n")
    print(f"Calculation took {end_optimized - start_optimized} seconds.")

    print("", end="", flush=True)
    time.sleep(0.01)

    assert pi_result == pi_result_optimized



