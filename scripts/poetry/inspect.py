from subprocess import check_call

import click


@click.command()
@click.option(
    "-b", "--block-number", type=str, help="the block number you are targetting"
)
@click.option(
    "-r", "--rpc", help="rpc endpoint, this needs to have parity style traces"
)
def inspect(block_number: str, rpc: str):
    check_call(
        [
            "docker",
            "compose",
            "exec",
            "mev-inspect",
            "python",
            "./scripts/inspect_block.py",
            block_number,
            rpc,
        ]
    )
