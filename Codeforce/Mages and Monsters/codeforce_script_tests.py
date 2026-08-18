import sys

import pathlib
import logging
import filecmp

import codeforce_script
from codeforce_script import log


only_run_these_tests: list[str] = []
# only_run_these_tests: list[str] = ["test-34"]

if __name__ == "__main__":
    log.setLevel(logging.DEBUG)

    if only_run_these_tests:
        log.info(f"Running tests only for {only_run_these_tests}")

    default_stdin = sys.stdin
    default_stdout = sys.stdout

    failed_tests:list[str] = []

    for in_path in pathlib.Path(__file__).parent.glob("inputs/*.txt"):
        if only_run_these_tests and all(test_name not in in_path.name for test_name in only_run_these_tests):
            continue

        sys.stdin = in_path.open(mode="r")

        out_path = in_path.parent.parent / "outputs" / in_path.name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        sys.stdout = out_path.open(mode="w")

        log.info(f"Starting {in_path.name.removesuffix('.txt')}...")

        codeforce_script.main()

        sys.stdin.close()
        sys.stdout.close()

        expected_out_path = in_path.parent.parent / "expected-outputs" / in_path.name

        if not filecmp.cmp(expected_out_path, out_path):
            log.error(f"Test for {in_path.name} failed")
            failed_tests.append(in_path.name)

        log.info("\n")


    sys.stdin = default_stdin
    sys.stdout = default_stdout

    if failed_tests:
        log.error(f"!!Found {len(failed_tests)} failed tests!!\n")
    for i, failed_test in enumerate(failed_tests, start=1):
        log.error(f"{i}: {failed_test.removesuffix('.txt')} failed")