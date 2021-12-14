from hashlib import sha3_256
from typing import List

import pytest

from mev_inspect.classifiers.trace import TraceClassifier


@pytest.fixture(scope="session")
def trace_classifier() -> TraceClassifier:
    return TraceClassifier()


@pytest.fixture(name="get_transaction_hashes")
def fixture_get_transaction_hashes():
    def _get_transaction_hashes(n: int):
        return _hash_with_prefix(n, "transaction_hash")

    return _get_transaction_hashes


@pytest.fixture(name="get_addresses")
def fixture_get_addresses():
    def _get_addresses(n: int):
        return [f"0x{hash_value[:40]}" for hash_value in _hash_with_prefix(n, "addr")]

    return _get_addresses


def _hash_with_prefix(n_hashes: int, prefix: str) -> List[str]:
    return [
        sha3_256(f"{prefix}{i}".encode("utf-8")).hexdigest() for i in range(n_hashes)
    ]
