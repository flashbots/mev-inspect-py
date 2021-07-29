from subprocess import check_call

import click


@click.command()
@click.option("--block-number", type=int, help="the block number you are targetting")
@click.option("--rpc", help="rpc endpoint, this needs to have parity style traces")
def inspect(block_number: int, rpc: str):
    check_call(
        [
            "docker",
            "compose",
            "exec",
            "mev-inspect",
            "python",
            "inspect_block.py",
            str(block_number),
            rpc,
        ]
    )
