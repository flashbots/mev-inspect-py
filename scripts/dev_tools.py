from subprocess import check_call

def lint():
    check_call(['pylint', '.'])

def test():
    check_call(['pytest', '--cov=mev_inspect', 'tests'])

def isort():
    check_call(['isort', '.'])

def isortcheck():
    check_call(['isort', '--diff', '.'])

def mypy():
    check_call(['mypy', '.'])

def black():
    check_call(['black', '.'])

def blackcheck():
    check_call(['black', '--diff', '--color', '.'])

def start():
    check_call(['docker', 'compose', 'up'])

def start_background():
    check_call(['docker', 'compose', 'up', '-d'])

def stop():
    check_call(['docker', 'compose', 'down'])

def build():
    check_call(['docker', 'compose', 'build'])

