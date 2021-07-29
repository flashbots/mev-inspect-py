from subprocess import check_call
import click


def lint():
    check_call(["pylint", "."])


def test():
    check_call(["pytest", "--cov=mev_inspect", "tests"])


@click.command()
@click.option("-c", required=False, is_flag=True)
def isort(c: str):
    """if c is present run isort in diff mode"""
    if c:
        check_call(["isort", "."])
    else:
        check_call(["isort", "--diff", "."])


def mypy():
    check_call(["mypy", "."])


@click.command()
@click.option("-c", required=False, is_flag=True)
def black(c: str):
    """if c is present run black in diff mode"""
    if c:
        check_call(["black", "."])
    else:
        check_call(["black", "--diff", "--color", "."])
