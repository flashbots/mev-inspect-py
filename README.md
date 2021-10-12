# mev-inspect-py

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
![Discord](https://img.shields.io/discord/755466764501909692)

[Maximal extractable value](https://ethereum.org/en/developers/docs/mev/) inspector for Ethereum, to illuminate the [dark forest](https://www.paradigm.xyz/2020/08/ethereum-is-a-dark-forest/) 🌲💡

Given a block, mev-inspect finds:
- miner payments (gas + coinbase)
- tokens transfers and profit
- swaps and [arbitrages](https://twitter.com/bertcmiller/status/1427632028263059462)
- ...and more

Data is stored in Postgres for analysis.

## Install

mev-inspect-py is built to run on kubernetes locally and in production.

### Dependencies

- [docker](https://www.docker.com/products/docker-desktop)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [helm](https://helm.sh/docs/intro/install/)

### Set up

Ceate a new cluster with:

```
kind create cluster
```

Set an environment variable `RPC_URL` to an RPC for fetching blocks.

Example:

```
export RPC_URL="http://111.111.111.111:8546"
```

**Note: mev-inspect-py currently requires an RPC of a full archive node with support for Erigon traces and receipts (not geth 😔)**

Next, start all services with:

```
tilt up
```

Press "space" to see a browser of the services starting up.

On first startup, you'll need to apply database migrations with:

```
kubectl exec deploy/mev-inspect -- alembic upgrade head
```

## Usage

### Inspect a single block

Inspecting block [12914944](https://twitter.com/mevalphaleak/status/1420416437575901185):

```
kubectl exec deploy/mev-inspect -- poetry run inspect-block 12914944
```

### Inspect many blocks

Inspecting blocks 12914944 to 12914954:

```
kubectl exec deploy/mev-inspect -- poetry run inspect-many-blocks 12914944 12914954
```

### Inspect all incoming blocks

Start a block listener with:

```
kubectl exec deploy/mev-inspect -- /app/listener start
```

By default, it will pick up wherever you left off.
If running for the first time, listener starts at the latest block.

See logs for the listener with:

```
kubectl exec deploy/mev-inspect -- tail -f listener.log
```

And stop the listener with:

```
kubectl exec deploy/mev-inspect -- /app/listener stop
```

### Exploring

All inspect output data is stored in Postgres.

To connect to the local Postgres database for querying, launch a client container with:

```
kubectl run -i --rm --tty postgres-client --env="PGPASSWORD=password" --image=jbergknoff/postgresql-client -- mev_inspect --host=postgresql --user=postgres
```

When you see the prompt:

```
mev_inspect=#
```

You're ready to query!

Try finding the total number of swaps decoded with UniswapV3Pool:

```
SELECT COUNT(*) FROM swaps WHERE abi_name='UniswapV3Pool';
```

or top 10 arbs by gross profit that took profit in WETH:

```
SELECT *
FROM arbitrages
WHERE profit_token_address = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
ORDER BY profit_amount DESC
LIMIT 10;
```

Postgres tip: Enter `\x` to enter "Explanded display" mode which looks nicer for results with many columns.

## FAQ

### How do I delete / reset my local postgres data?

Stop the system if running:

```
tilt down
```

Delete it with:

```
kubectl delete pvc data-postgresql-postgresql-0
```

Start back up again:

```
tilt up
```

And rerun migrations to create the tables again:

```
kubectl exec deploy/mev-inspect -- alembic upgrade head
```

### I was using the docker-compose setup and want to switch to kube, now what?

Re-add the old `docker-compose.yml` file to your mev-inspect-py directory.

A copy can be found [here](https://github.com/flashbots/mev-inspect-py/blob/ef60c097719629a7d2dc56c6e6c9a100fb706f76/docker-compose.yml)

Tear down docker-compose resources:

```
docker compose down
```

Then go through the steps in the current README for kube setup.

### Error from server (AlreadyExists): pods "postgres-client" already exists

This means the postgres client container didn't shut down correctly.

Delete this one with:

```
kubectl delete pod/postgres-client
```

Then start it back up again.

## Maintainers

- [@lukevs](https://github.com/lukevs)

## Contributing

[Flashbots](https://flashbots.net) is a research and development collective working on mitigating the negative externalities of decentralized economies. We contribute with the larger free software community to illuminate the dark forest.

You are welcome here <3.

- If you want to join us, come and say hi in our [Discord chat](https://discord.gg/7hvTycdNcK).
- If you have a question, feedback or a bug report for this project, please [open a new Issue](https://github.com/flashbots/flashbots-repository-template/issues).
- If you would like to contribute with code, check the [CONTRIBUTING file](CONTRIBUTING.md).
- We just ask you to be nice.

## Security

If you find a security vulnerability on this project or any other initiative related to Flashbots, please let us know sending an email to security@flashbots.net.

---

Made with ☀️  by the ⚡🤖 collective.
