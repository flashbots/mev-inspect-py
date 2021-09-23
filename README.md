# mev-inspect-py
> illuminating the dark forest 🌲💡

**mev-inspect-py** is an MEV inspector for Ethereum

Given a block, mev-inspect finds:
- miner payments (gas + coinbase)
- tokens transfers and profit
- swaps and [arbitrages](https://twitter.com/bertcmiller/status/142763202826305946://twitter.com/bertcmiller/status/1427632028263059462)
- ...and more

Data is stored in Postgres for analysis

## Running locally
mev-inspect-py is built to run on kubernetes locally and in production

### Install dependencies

First, setup a local kubernetes deployment - we use [kind](https://kind.sigs.k8s.io/docs/user/quick-start)

If using kind, create a new cluster with:
```
kind create cluster
```

Next, install the kubernetes CLI [`kubectl`](https://kubernetes.io/docs/tasks/tools/)

Then, install [helm](https://helm.sh/docs/intro/install/) - helm is a package manager for kubernetes

Lastly, setup [Tilt](https://docs.tilt.dev/install.html) which manages running and updating kubernetes resources locally

### Start up

Set an environment variable `RPC_URL` to an RPC for fetching blocks
Example:
```
export RPC_URL="http://111.111.111.111:8546"
```

**Note: mev-inspect-py currently requires and RPC with support for parity traces**

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

Inspecting block [12914944](https://twitter.com/mevalphaleak/status/1420416437575901185)
```
kubectl exec deploy/mev-inspect-deployment -- poetry run inspect-block 12914944
```

### Inspect many blocks

Inspecting blocks 12914944 to 12914954
```
kubectl exec deploy/mev-inspect-deployment -- poetry run inspect-many-blocks 12914944 12914954
```

### Inspect all incoming blocks

Start a block listener with
```
kubectl exec deploy/mev-inspect-deployment -- /app/listener start
```

By default, it will pick up wherever you left off.
If running for the first time, listener starts at the latest block

See logs for the listener with
```
kubectl exec deploy/mev-inspect-deployment -- tail -f listener.log
```

And stop the listener with
```
kubectl exec deploy/mev-inspect-deployment -- /app/listener stop
```

## Contributing

### Guide

✨ Coming soon

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

### Tests

Run tests with
```
kubectl exec deploy/mev-inspect-deployment -- poetry run pytest --cov=mev_inspect tests
```

## FAQ

### How do I delete / reset my local postgres data?

Stop the system if running
```
tilt down
```

Delete it with
```
kubectl delete pvc data-postgresql-postgresql-0
```

Start back up again
```
tilt up
```

And rerun migrations to create the tables again
```
kubectl exec deploy/mev-inspect-deployment -- alembic upgrade head
```

### I was using the docker-compose setup and want to switch to kube, now what?

Re-add the old `docker-compose.yml` file to your mev-inspect-py directory

A copy can be found [here](https://github.com/flashbots/mev-inspect-py/blob/ef60c097719629a7d2dc56c6e6c9a100fb706f76/docker-compose.yml)

Tear down docker-compose resources
```
docker compose down
```

Then go through the steps in the current README for kube setup
