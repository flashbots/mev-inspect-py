# mev-inspect
A [WIP] Ethereum MEV Inspector in Python managed by Poetry

## Containers
mev-inspect's local setup is built on [Docker Compose](https://docs.docker.com/compose/)

By default it starts up:
- `mev-insepct` - a container with the code in this repo used for running scripts
- `db` - a postgres database instance
- `pgadmin` - a postgres DB UI for querying and more (avaiable at localhost:5050)

## Running locally
Setup [Docker](https://www.docker.com/products/docker-desktop)
Setup [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)

Install dependencies through poetry
```
poetry install
```

Start the services (optionally as background processes)
```
poetry run start [-b]
```

Apply the latest migrations against the local DB:
```
poetry run exec alembic upgrade head
``` 

Run inspect on a block
```
poetry run inspect --block-number 11931270 --rpc 'http://111.11.11.111:8545/'
``` 

To stop the services (if running in the background, otherwise just ctrl+c)
```
poetry run stop
```

MEV container can be attached via
```
poetry run attach
```

Running additional compose commands are possible through standard `docker
compose ...` calls.  Check `docker compose help` for more tools available

## Executing scripts
Any script can be run from the mev-inspect container like
```
poetry run exec <your command here>
```

For example
```
poetry run exec python examples/uniswap_inspect.py -block_number=123 -rpc='111.111.111'
```

### Poetry Scripts
```bash
# code check
poetry run lint # linting via Pylint
poetry run test # testing and code coverage with Pytest
poetry run isort # fixing imports 
poetry run mypy # type checking 
poetry run black # style guide 
poetry run pre-commit run --all-files # runs Black, PyLint and MyPy
# docker management
poetry run start [-b] # starts all services, optionally in the background
poetry run stop # shutsdown all services or just ctrl + c if foreground
poetry run build # rebuilds containers
poetry run attach # enters the mev-inspect container in interactive mode
# launches inspection script
poetry run inspect --block-number 11931270 --rpc 'http://111.11.11.111:8545/'
```


## Rebuilding containers
After changes to the app's Dockerfile, rebuild with
```
poetry run build
```

## Using PGAdmin

1. Go to [localhost:5050](localhost:5050)

2. Login with the PGAdmin username and password in `.env`

3. Add a new engine for mev_inspect with
    - host: db
    - user / password: see `.env`

## Contributing

Pre-commit is used to maintain a consistent style, prevent errors and ensure test coverage. 

Install pre-commit with:
```
poetry run pre-commit install
```

Update README if needed
