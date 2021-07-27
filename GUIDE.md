# Contributor guide

### Requirements

* [Install](https://docs.docker.com/compose/install/) docker compose
    * To run `mev-inspect`, `postgres`, and `pgadmin` within a local container.
* Python
    * Our pre-commit hook requires v3.9, use pyenv to manage versions and venv, instructions [here](https://www.andreagrandi.it/2020/10/10/install-python-with-pyenv-create-virtual-environment-with-specific-python-version/).
    * Verify with `pre-commit install && pre-commit run --all-files` 
* Archive node with `trace_*` rpc module (Erigon/OpenEthereum)

    * If you do not have access to an archive node, reach out to us on our [discord](https://discord.gg/5NB53YEGVM) for raw traces (of the blocks with MEV you're writing inspectors for) or an rpc endpoint.
### Quick start

We use poetry for python package management, start with installing the required libraries: 
* `poetry install`

Build the container:
* `poetry run build`

Run a specifc inspector:
* `poetry run inspect -script ./examples/uniswap_inspect.py -block_number 12901446 -rpc 'http://localhost:8545'`

Or directly using docker: 
* `docker compose exec mev-inspect python testing_file.py -block_number 12901446 -rpc 'http://localhost:8545'`

You will be able to run all the inspectors against a specific transaction, block, and range of blocks once we finalize our data model/architecture but for now, write a protocol specifc inspector script and verify against a test block (with the MEV you're trying to quantify). 

Full list of poetry commands for this repo can be found [here](https://github.com/flashbots/mev-inspect-py#poetry-scripts). 


### Tracing

While simple ETH and token transfers are trivial to parse/filter (by processing their transaction input data, events and/or receipts), contract interactions can be complex to identify. EVM tracing allows us to dig deeper into the transaction execution cycle to look through the internal calls and any other additional proxy contracts the tx interacts with.

Trace types (by `action_type`):

* `Call`, which is returned when a method on a contract (same as the tx `to` field or a different one within) is executed. We can identify the input parameters in each instance by looking at this sub trace. 
* `Self-destruct`, when a contract destroys the code at its address and transfers the ETH held in the contract to an EOA. Common pattern among arbitrage bots given the gas refund savings. 
* `Create`, when a contract deploys another contract and transfers assets to it. 
* `Reward`, pertaining to the block reward and uncle reward, not relevant here. 

Note that this is for Erigon/OpenEthereum `trace` module and Geth has a different tracing mechanism that is more low-level/irrelevant for inspect.

### Architecture

TODO: Actions, inspectors, reducers context

TODO: Single tx vs multi tx context

#### Inspectors

TODO: list done/wip/current

#### Tokenflow

The method iterates over all the traces and makes a note of all the ETH inflows/outflows as well as stablecoins (USDT/USDC/DAI) for the `eoa`, `contract`, `proxy`. Once it is done, it finds out net profit by subtracting the gas spent from the MEV revenue. All profits will be converted to ETH, based on the exchange rate at that block height. 

Example: https://etherscan.io/tx/0x4121ce805d33e952b2e6103a5024f70c118432fd0370128d6d7845f9b2987922

ETH=>ENG=>ETH across DEXs

Script output: 
EOA: 0x00000098163d8908dfbd126c873c9c4732a2c2e6
Contract: 0x000000000000006f6502b7f2bbac8c30a3f67e9a
Tx proxy: 0x0000000000000000000000000000000000000000
Stablecoins inflow/outflow: [0, 0]
Net ETH profit, Wei 22357881284770142 

#### Database

Final `mev_inspections` table schema:

* As of `mev-inspect-rs`:
    * hash
    * status
        * `Success` or `Reverted`
    * block_number
    * gas_price
    * revenue
        * Revenue searcher makes after accounting for gas used.
    * protocols
        * Different protocols that we identify the transaction to touch
    * actions
        * Different relevant actions parsed from the transaction traces
    * eoa
        * EOA address that initiates the transaction
    * contract
        * `to` field, either a custom contract utilized for a searcher to capture MEV or a simple router
    * proxy_impl
        * Proxy implementations used by searchers, if any
    * inserted_at

Additional fields we're interested in: 
* miner
    * Coinbase address of the block miner
* eth_usd_price
    * Price of ETH that block height
    * Similarly, for any tokens (say in an arbitrage inspection) we query against the relevant uniswap pools.
* tail_gas_price
    * Gas price of the transaction displaced in the block (last tx that would've otherwise)
* token_flow_estimate
    * Profit outputted by the token flow function
* delta
    * Difference between profit estimated by our inspectors and pure token flow analysis


[Creating an inspector from scratch](./CreateInspector.md)


