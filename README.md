# mev-inspect
An MEV inspector for Ethereum

## Running locally
mev-inspect-py is built to run on kubernetes locally and in production

### Install dependencies

Setup a local kubernetes deployment (we use [kind](https://kind.sigs.k8s.io/docs/user/quick-start))
Setup [Tilt](https://docs.tilt.dev/install.html) which manages the local deployment

### Start up

Set an environment variable `RPC_URL` to an RPC for fetching blocks
Example:
```
export RPC_URL="http://111.111.111.111:8546"
```

Note: mev-inspect-py currently requires and RPC with support for parity traces

Next, start all servcies with:
```
tilt up
```

Press "space" to see a browser of the services starting up

On first startup, you'll need to apply database migrations. Apply with:
```
kubectl exec deploy/mev-inspect-deployment -- alembic upgrade head
```

## Inspecting

### Inspect a single block
### Inspect many blocks
### Inspect all incoming blocks

## Database migrations

### Creating a new database migration

## Contributing

### Guide

Coming soon

### Pre-commit

We use pre-commit to maintain a consistent style, prevent errors, and ensure test coverage. 

To set up, install dependencies through poetry
```
poetry install
```

Then install pre-commit hooks with
```
poetry run pre-commit install
```
