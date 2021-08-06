from subprocess import check_call

import click


@click.command()
@click.option(
    "-b", "--block-number", type=str, help="the block number you are targetting"
)
@click.option(
    "-r", "--rpc", help="rpc endpoint, this needs to have parity style traces"
)
@click.option(
    "--cache/--no-cache",
    help="whether to read / write to the cache",
    default=True,
)
def inspect(block_number: str, rpc: str, cache: bool):
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
            "--cache" if cache else "--no-cache",
        ]
    )


@click.command()
@click.argument("after_block", type=str)
@click.argument("before_block", type=str)
@click.argument("rpc")
@click.option(
    "--cache/--no-cache",
    help="whether to read / write to the cache",
    default=True,
)
def inspect_many(after_block: str, before_block: str, rpc: str, cache: bool):
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
            "--cache" if cache else "--no-cache",
        ]
    )
