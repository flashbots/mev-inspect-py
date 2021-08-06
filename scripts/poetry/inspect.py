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
            "inspect-block",
            block_number,
            rpc,
        ]
    )


@click.command()
@click.option("--after-block", type=str, help="look at blocks after this number")
@click.option("--before-block", type=str, help="look at blocks before this number")
@click.option(
    "-r", "--rpc", help="rpc endpoint, this needs to have parity style traces"
)
def inspect_many(after_block: str, before_block: str, rpc: str):
    check_call(
        [
            "docker",
            "compose",
            "exec",
            "mev-inspect",
            "python",
            "./scripts/inspect_block.py",
            "inspect-many-blocks",
            after_block,
            before_block,
            rpc,
        ]
    )
