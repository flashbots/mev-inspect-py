
# Running mev-inspect-py without kubernetes ('monolithic mode')

Running mev-inspect-py outside of kubernetes can be useful for debug purposes. In this case, the steps for installation are:
1. Install dependencies (pyenv, poetry, postgres)
1. Set up python virtual environment using matching python version (3.9.x) and install required python modules using poetry
1. Create postgres database
1. Run database migrations

The database credentials and archive node address used by mev-inspect-py need to be loaded into environment variables (both for database migrations and to run mev-inspect-py).

## Ubuntu install instructions

So, starting from a clean Ubuntu 22.04 installation, the prerequisites for pyenv, psycopg2 (python3-dev libpq-dev) can be installed with

`sudo apt install -y make build-essential git libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev liblzma-dev python3-dev libpq-dev`

### pyenv
Install pyenv using the web installer

`curl https://pyenv.run | bash`

and add the following to `~/.bashrc` (if running locally) or `~/.profile` (if running over ssh).

```
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Then update the current shell by running `source ~/.bashrc` or `source ~/.profile` as appropriate.

### Poetry

Install Poetry using the web installer

`curl -sSL https://install.python-poetry.org | python3 -`

add the following to `~/.bashrc` (if running locally) or `~/.profile` (if running over ssh)

`export PATH="/home/user/.local/bin:$PATH"`

If running over ssh you should also add the following to `~/.profile` to prevent [Poetry errors](https://github.com/python-poetry/poetry/issues/1917) from a lack of active keyring:

`export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring`

Again update current shell by running `source ~/.bashrc` or `source ~/.profile` as appropriate.

### postgres
We have tested two alternatives for postgres - installing locally or as a container.

#### Option 1: Installing locally

To install locally from a clean Ubuntu 22.04 installation, run:
`sudo apt install postgresql postgresql-contrib`

Note: You may need to reconfigure your pg-hba.conf to allow local access.

#### Option 2: Installing docker

To avoid interfering with your local postgres instance, you may prefer to run postgres within a docker container.
For docker installation instructions, please refer to https://docs.docker.com/engine/install/ubuntu/

### mev-inspect-py

With all dependencies now installed, clone the mev-inspec-py repo
```
git clone https://github.com/flashbots/mev-inspect-py.git
cd mev-inspect-py
```
We now install the required pythn version and use Poetry to install the required python modules into a virtual environment. 

```
pyenv install 3.9.16
pyenv local 3.9.16
poetry env use 3.9.16
poetry install
```

### Create database
mev-inspect-py outputs to a postgres database, so we need to set this up. There are various ways of doing this, two options are presented here.

#### Option 1 — Run postgres locally
```
sudo -u postgres psql
\password
postgres
create database mev_inspect;
\q
```

#### Option 2 — Use postgres docker image
To avoid interfering with your local postgres instance, you may prefer to run postgres within a docker container. First ensure that postgres is not currently running to ensure port `5432` is available:
`sudo systemctl stop postgresql`
and then start a containerised postgres instance:
`sudo docker run -d -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=mev_inspect postgres`

### Environment variables
We will need to set a few environment variables to use mev-inspect-py. **These will be required every time mev-inspect-py runs**, so again you may wish to add these to your `~/.bashrc` and/or `~/.profile` as appropriate. Note that you need to substitute the correct URL for your archive node below if you are not running Erigon locally.
```
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export RPC_URL="http://127.0.0.1:8545"
```
### Database migrations
Finally run the database migrations and fetch price information:

```
poetry run alembic upgrade head
poetry run fetch-all-prices
```

## Usage instructions
The same functionality available through kubernetes can be run in 'monolithic mode', but the relevant functions now need to be invoked by Poetry directly. So to inspect a single block, run for example:

`poetry run inspect-block 16379706`

Or to inspect a range of blocks:

`poetry run inspect-many-blocks 16379606 16379706`

Or to run the test suite:

`poetry run pytest tests`

