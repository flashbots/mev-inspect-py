# mev-inspect
A [WIP] Ethereum MEV Inspector in Python

## Containers
mev-inspect's local setup is built on [Docker Compose](https://docs.docker.com/compose/)

By default it starts up:
- `mev-insepct` - a container with the code in this repo used for running scripts
- `db` - a postgres database instance
- `pgadmin` - a postgres DB UI for querying and more (avaiable at localhost:5050)

## Running locally
Setup [Docker](https://www.docker.com/products/docker-desktop)

Start the services with Docker Compose
```
docker compose up
```
or to run in the background
```
docker compose up -d
```

To stop the services (if running in the background, otherwise just ctrl+c)
```
docker compose down
```

Check `docker compose help` for more tools available

## Executing scripts
To run a command, prefix it with
```
docker compose exec mev-inspect <YOUR COMMAND>
```

For example, to run `testing_file.py`:
```
docker compose exec mev-inspect python testing_file.py \
    -block_number 11931271 \
    -rpc 'http://111.11.11.111:8545'
```

Or to run the tests:
```
docker compose exec mev-inspect python -m unittest tests/*py
```

## Rebuilding containers
After changes to the app's Dockerfile, rebuild with
```
docker compose build
```

## Using PGAdmin

1. Go to [localhost:5050](localhost:5050)

2. Login with the PGAdmin username and password in `.env`

3. Add a new engine for mev_inspect with
    - host: db
    - user / password: see `.env`

## Contributing
Contributing requires installing the pre-commit hooks

1 . Ensure you're using python 3.9

If not, [pyenv](https://github.com/pyenv/pyenv) is a great option for managing python versions

2. Create a virtualenv
```
python3 -m venv venv
```

3. Activate it
```
. venv/bin/activate
```
(exit with `deactivate`)

4. Install dev libraries
```
pip install -r requirements_dev.txt
```

5. Install pre-commit
```
pre-commit install
```

6. Install pre-commit's dependencies and ensure that it's working
```
pre-commit run --all-files
```
