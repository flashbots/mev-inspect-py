# mev-inspect-py

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![Discord](https://img.shields.io/discord/755466764501909692)](https://discord.gg/7hvTycdNcK)

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
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start), or a similar tool for running local Kubernetes clusters
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [helm](https://helm.sh/docs/intro/install/)
- [tilt](https://docs.tilt.dev/install.html)

### Set up

Create a new cluster with:

```
kind create cluster
```

Set an environment variable `RPC_URL` to an RPC for fetching blocks.

mev-inspect-py currently requires a node with support for Erigon traces and receipts (not geth yet 😔).

[pokt.network](https://www.pokt.network/)'s "Ethereum Mainnet Archival with trace calls" is a good hosted option.

Example:

```
export RPC_URL="http://111.111.111.111:8546"
```


Next, start all services with:

```
tilt up
```

Press "space" to see a browser of the services starting up.

On first startup, you'll need to apply database migrations with:

```
./mev exec alembic upgrade head
```

And load prices data

```
./mev prices fetch-all
```

## Monolithic (non-kubernetes) install instructions

For an alternative means of running mev-inspect-py for smaller set-ups or debug purposes see the [monolithic install instructions](MONOLITHIC.md).

## Usage

### Inspect a single block

Inspecting block [12914944](https://twitter.com/mevalphaleak/status/1420416437575901185):

```
./mev inspect 12914944
```

### Inspect many blocks

Inspecting blocks 12914944 to 12914954:

```
./mev inspect-many 12914944 12914954
```

### Inspect all incoming blocks

Start a block listener with:

```
./mev listener start
```

By default, it will pick up wherever you left off.
If running for the first time, listener starts at the latest block.

Tail logs for the listener with:

```
./mev listener tail
```

And stop the listener with:

```
./mev listener stop
```

### Backfilling

For larger backfills, you can inspect many blocks in parallel

To inspect blocks 12914944 to 12915044, run
```
./mev backfill 12914944 12915044
```

This queues the blocks in Redis to be pulled off by the mev-inspect-worker service

To increase or decrease parallelism, update the replicaCount value for the mev-inspect-workers helm chart

Locally, this can be done by editing Tiltfile and changing "replicaCount=1" to your desired parallelism:
```
k8s_yaml(helm(
    './k8s/mev-inspect-workers',
    name='mev-inspect-workers',
    set=["replicaCount=1"],
))
```

You can see worker pods spin up then complete by watching the status of all pods
```
watch kubectl get pods
```

To see progress and failed batches, connect to Redis with
```
./mev redis
```

For total messages, query:
```
HLEN dramatiq:default.msgs
```

For messages failed and waiting to retry in the delay queue (DQ), query:
```
HGETALL dramatiq:default.DQ.msgs
```

For messages permanently failed in the dead letter queue (XQ), query:
```
HGETALL dramatiq:default.XQ.msgs
```

To clear the queue, delete keys for the main queue and delay queue
```
DEL dramatiq:default.msgs
DEL dramatiq:default.DQ.msgs
```

For more information on queues, see the [spec shared by dramatiq](https://github.com/Bogdanp/dramatiq/blob/24cbc0dc551797783f41b08ea461e1b5d23a4058/dramatiq/brokers/redis/dispatch.lua#L24-L43)

**Backfilling a list of blocks**

Create a file containing a block per row, for example blocks.txt containing:
```
12500000
12500001
12500002
```

Then queue the blocks with
```
cat blocks.txt | ./mev block-list
```

To watch the logs for a given worker pod, take its pod name using the above, then run:
```
kubectl logs -f pod/mev-inspect-worker-abcdefg
```

(where `mev-inspect-worker-abcdefg` is your actual pod name)


### Exploring

All inspect output data is stored in Postgres.

To connect to the local Postgres database for querying, launch a client container with:

```
./mev db
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
kubectl delete pvc data-postgresql-0
```

Start back up again:

```
tilt up
```

And rerun migrations to create the tables again:

```
./mev exec alembic upgrade head
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
- [@gheise](https://github.com/gheise)
- [@bertmiller](https://github.com/bertmiller)

## Contributing

[Flashbots](https://flashbots.net) is a research and development collective working on mitigating the negative externalities of decentralized economies. We contribute with the larger free software community to illuminate the dark forest.

You are welcome here <3.

- If you want to join us, come and say hi in our [Discord chat](https://discord.gg/7hvTycdNcK).
- If you have a question, feedback or a bug report for this project, please [open a new Issue](https://github.com/flashbots/mev-inspect-py/issues).
- If you would like to contribute with code, check the [CONTRIBUTING file](CONTRIBUTING.md).
- We just ask you to be nice.

## Security

If you find a security vulnerability on this project or any other initiative related to Flashbots, please let us know sending an email to security@flashbots.net.

---

Made with ☀️  by the ⚡🤖 collective.
