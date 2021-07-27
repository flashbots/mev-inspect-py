from subprocess import check_call
import click


@click.command()
@click.option("-b", required=False, is_flag=True)
def start(b: str):
    """if d is present background compose"""
    if b:
        check_call(["docker", "compose", "up", "-d"])
        click.echo("docker running in the background...")
    else:
        check_call(["docker", "compose", "up"])


def stop():
    check_call(["docker", "compose", "down"])


def build():
    check_call(["docker", "compose", "build"])


def attach():
    check_call(["docker", "exec", "-it", "mev-inspect-py_mev-inspect_1", "bash"])


@click.command()
@click.option("-script", help="inspect script", default="./examples/uniswap_inspect.py")
@click.option("-block_num", help="block number to inspect", default=11931271)
@click.option("-rpc", help="rpc address", default="http://111.11.11.111:8545")
def inspect(script: str, block_num: int, rpc: str):
    """Runs mev-inspect scripts through docker services"""
    check_call(
        [
            "docker",
            "compose",
            "exec",
            "mev-inspect",
            "python",
            script,
            f"-block_number {block_num}",
            f"-rpc {rpc}",
        ]
    )
