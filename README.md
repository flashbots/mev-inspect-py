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

Start the services (optionally as background processes)
```
poetry run start [-b]
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
Inspection is the only simplified api available through poetry at the moment
with a more generalized api on the horizon.

Inspect scripts must have `-script`, `-block_number` and `-rpc` arguments.
Using the uniswap inspect from `./examples`
```
poetry run inspect -script ./examples/uniswap_inspect.py -block_number 11931271 \
                   -rpc 'http://111.11.11.111:8545'
```

Generalized user defined scripts can still be run through the docker interface as
```
docker compose exec mev-inspect python testing_file.py \
    -block_number 11931271 \
    -rpc 'http://111.11.11.111:8545'
```
### Poetry Scripts
```bash
# code check
poetry run lint # linting via Pylint
poetry run test # testing and code coverage with Pytest
poetry run isort # fixing imports 
poetry run mypy # type checking 
poetry run black # style guide 
poetry run pre-commit # runs Black, PyLint and MyPy
# docker management
poetry run start [-b] # starts all services, optionally in the background
poetry run stop # shutsdown all services or just ctrl + c if foreground
poetry run build # rebuilds containers
poetry run attach # enters the mev-inspect container in interactive mode
# launches inspection script
poetry run inspect -script ... -block_number ... -rpc ...
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
Development can be done locally or in the docker container.  Use local if
contributions can be fully tested without invoking the database related
services.

1. Install dependencies and build python environment
```
poetry install
```
or with docker
```
poetry run build
```
2. Pre-commit is used to maintain a consistent style, prevent errors and ensure
   test coverage.  Make sure to fix any errors presented via Black, Pylint and
   MyPy pre-commit hooks
```
poetry run pre-commit --all-files
```
or within docker
```
pre-commit run --all-files
```
3. Update README if needed
