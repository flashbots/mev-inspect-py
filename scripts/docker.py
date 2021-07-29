from subprocess import check_call
from typing import List

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
@click.argument("args", nargs=-1)
def exec(args: List[str]):
    check_call(["docker", "compose", "exec", "mev-inspect", *args])
