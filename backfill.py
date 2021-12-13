import subprocess
import sys

from typing import Iterator, Tuple


def get_block_after_before_chunks(
    after_block: int,
    before_block: int,
    n_workers: int,
) -> Iterator[Tuple[int, int]]:
    n_blocks = before_block - after_block
    remainder = n_blocks % n_workers
    floor_chunk_size = n_blocks // n_workers

    last_before_block = None

    for worker_index in range(n_workers):
        chunk_size = floor_chunk_size

        if worker_index < remainder:
            chunk_size += 1

        batch_after_block = (
            last_before_block if last_before_block is not None else after_block
        )

        batch_before_block = batch_after_block + chunk_size
        yield batch_after_block, batch_before_block
        last_before_block = batch_before_block


def backfill(after_block: int, before_block: int, n_workers: int):
    if n_workers <= 0:
        raise ValueError("Need at least one worker")

    for batch_after_block, batch_before_block in get_block_after_before_chunks(
        after_block,
        before_block,
        n_workers,
    ):
        print(f"Backfilling {batch_after_block} to {batch_before_block}")
        backfill_command = f"sh backfill.sh {batch_after_block} {batch_before_block}"
        process = subprocess.Popen(backfill_command.split(), stdout=subprocess.PIPE)
        output, _ = process.communicate()
        print(output)


def main():
    after_block = int(sys.argv[1])
    before_block = int(sys.argv[2])
    n_workers = int(sys.argv[3])

    backfill(after_block, before_block, n_workers)


if __name__ == "__main__":
    main()
