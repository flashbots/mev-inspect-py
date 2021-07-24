import click
from subprocess import check_call, run
from typing import List

@click.command()
@click.option('-b', required=False, is_flag=True)
def start(b: str):
    '''if d is present background compose'''
    if b:
        check_call(['docker', 'compose', 'up', '-d'])
        click.echo('docker running in the background...')
    else:
        check_call(['docker', 'compose', 'up'])

def stop():
    check_call(['docker', 'compose', 'down'])

def build():
    check_call(['docker', 'compose', 'build'])
