from typing import List, Optional

from mev_inspect.schemas import Block, Trace, TraceType

weth_address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

cache_directory = "./cache"


def is_stablecoin_address(address):
    # to look for stablecoin inflow/outflows
    stablecoin_addresses = [
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
        "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
        "0x0000000000085d4780b73119b644ae5ecd22b376",  # TUSD
        "0x4fabb145d64652a948d72533023f6e7a623c7c53",  # BUSD
        "0x8e870d67f660d95d5be530380d0ec0bd388289e1",  # PAX
        "0x956F47F50A910163D8BF957Cf5846D573E7f87CA",  # FEI
        "0x853d955aCEf822Db058eb8505911ED77F175b99e",  # FRAX
        "0xBC6DA0FE9aD5f3b0d58160288917AA56653660E9",  # alUSD
        "0x57Ab1ec28D129707052df4dF418D58a2D46d5f51",  # sUSD
        "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",  # lUSD
        "0x674C6Ad92Fd080e4004b2312b45f796a192D27a0",  # USDN
    ]
    return address in stablecoin_addresses


def is_known_router_address(address):
    # to exclude known router addresses from token flow analysis
    known_router_addresses = [
        "0x3D71d79C224998E608d03C5Ec9B405E7a38505F0",  # keeper dao, whitelists extraction
        "0x11111254369792b2Ca5d084aB5eEA397cA8fa48B",  # 1inch v1 router
        "0x111111125434b319222cdbf8c261674adb56f3ae",  # 1inch v2 router
        "0x11111112542d85b3ef69ae05771c2dccff4faa26",  # 1inch v3 router
        "0xa356867fdcea8e71aeaf87805808803806231fdc",  # DODO
        "0xdef1c0ded9bec7f1a1670819833240f027b25eff",  # 0x proxy
        "0x90f765f63e7dc5ae97d6c576bf693fb6af41c129",  # Set Trade
        "0x7113dd99c79aff93d54cfa4b2885576535a132de",  # Totle exchange
        "0x9509665d015bfe3c77aa5ad6ca20c8afa1d98989",  # Paraswap
        "0x86969d29F5fd327E1009bA66072BE22DB6017cC6",  # Paraswap v2
        "0xf90e98f3d8dce44632e5020abf2e122e0f99dfab",  # Paraswap v3
        "0x57805e5a227937bac2b0fdacaa30413ddac6b8e1",  # Furucombo
        "0x17e8ca1b4798b97602895f63206afcd1fc90ca5f",  # Furucombo proxy
        "0x881d40237659c251811cec9c364ef91dc08d300c",  # Metamask swap
        "0x745daa146934b27e3f0b6bff1a6e36b9b90fb131",  # DEX.ag
        "0xb2be281e8b11b47fec825973fc8bb95332022a54",  # Zerion SDK
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  # UniswapV2Router02
        "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",  # SushiswapV2Router02
        "0xE592427A0AEce92De3Edee1F18E0157C05861564",  # Uniswap v3 router
        "0x3E66B66Fd1d0b02fDa6C811Da9E0547970DB2f21",  # Balance exchange proxy
        "0x1bD435F3C054b6e901B7b108a0ab7617C808677b",  # Paraswap v4
        "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",  # SNX proxy synth issuer
    ]
    return address in known_router_addresses


# we're interested in the to address to run token flow on it as well
def get_tx_to_address(tx_hash, block) -> Optional[str]:
    for receipt in block.receipts:
        if receipt.transaction_hash == tx_hash:
            return receipt.to

    return None


def get_tx_proxies(tx_traces: List[Trace], to_address: Optional[str]):
    proxies = []

    for trace in tx_traces:
        if (
            trace.type == TraceType.call
            and trace.action["callType"] == "delegatecall"
            and trace.action["from"] == to_address
        ):
            proxies.append(trace.action["to"])

    return proxies


def get_net_gas_used(tx_hash, block):
    gas_used = 0
    for trace in block.traces:
        if trace.transaction_hash == tx_hash:
            gas_used += int(trace.result["gasUsed"], 16)

    return gas_used


def get_ether_flows(tx_traces, addresses_to_check):
    eth_inflow = 0
    eth_outflow = 0

    for trace in tx_traces:
        if trace.type == TraceType.call:
            value = int(
                trace.action["value"], 16
            )  # converting from 0x prefix to decimal
            # ETH_GET
            if (
                trace.action["callType"] != "delegatecall"
                and trace.action["from"] != weth_address
                and value > 0
                and trace.action["to"] in addresses_to_check
            ):
                eth_inflow = eth_inflow + value

            # ETH_GIVE
            if (
                trace.action["callType"] != "delegatecall"
                and trace.action["to"] != weth_address
                and value > 0
                and trace.action["from"] in addresses_to_check
            ):
                eth_outflow = eth_outflow + value

            if trace.action["to"] == weth_address:
                # WETH_GET1 & WETH_GET2 (to account for both 'transfer' and 'transferFrom' methods)
                # WETH_GIVE1 & WETH_GIVE2

                # transfer(address to,uint256 value) with args
                if len(trace.action["input"]) == 138:
                    if trace.action["input"][2:10] == "a9059cbb":
                        transfer_to = "0x" + trace.action["input"][34:74]
                        transfer_value = int("0x" + trace.action["input"][74:138], 16)
                        if transfer_to in addresses_to_check:
                            eth_inflow = eth_inflow + transfer_value
                        elif trace.action["from"] in addresses_to_check:
                            eth_outflow = eth_outflow + transfer_value

                # transferFrom(address from,address to,uint256 value )
                if len(trace.action["input"]) == 202:
                    if trace.action["input"][2:10] == "23b872dd":
                        transfer_from = "0x" + trace.action["input"][34:74]
                        transfer_to = "0x" + trace.action["input"][98:138]
                        transfer_value = int("0x" + trace.action["input"][138:202], 16)
                        if transfer_to in addresses_to_check:
                            eth_inflow = eth_inflow + transfer_value
                        elif transfer_from in addresses_to_check:
                            eth_outflow = eth_outflow + transfer_value

        if trace.type == TraceType.suicide:
            if trace.action["refundAddress"] in addresses_to_check:
                refund_value = int("0x" + trace.action["balance"], 16)
                eth_inflow = eth_inflow + refund_value

    return [eth_inflow, eth_outflow]


def get_dollar_flows(tx_traces, addresses_to_check):
    dollar_inflow = 0
    dollar_outflow = 0
    for trace in tx_traces:
        if trace.type == TraceType.call and is_stablecoin_address(trace.action["to"]):
            _ = int(trace.action["value"], 16)  # converting from 0x prefix to decimal

            # USD_GET1 & USD_GET2 (to account for both 'transfer' and 'transferFrom' methods)
            # USD_GIVE1 & USD_GIVE2

            # transfer(address to,uint256 value) with args
            if len(trace.action["input"]) == 138:
                if trace.action["input"][2:10] == "a9059cbb":
                    transfer_to = "0x" + trace.action["input"][34:74]
                    transfer_value = int("0x" + trace.action["input"][74:138], 16)
                    if transfer_to in addresses_to_check:
                        dollar_inflow = dollar_inflow + transfer_value
                    elif trace.action["from"] in addresses_to_check:
                        dollar_outflow = dollar_outflow + transfer_value

            # transferFrom(address from,address to,uint256 value )
            if len(trace.action["input"]) == 202:
                if trace.action["input"][2:10] == "23b872dd":
                    transfer_from = "0x" + trace.action["input"][34:74]
                    transfer_to = "0x" + trace.action["input"][98:138]
                    transfer_value = int("0x" + trace.action["input"][138:202], 16)
                    if transfer_to in addresses_to_check:
                        dollar_inflow = dollar_inflow + transfer_value
                    elif transfer_from in addresses_to_check:
                        dollar_outflow = dollar_outflow + transfer_value
    return [dollar_inflow, dollar_outflow]


def run_tokenflow(tx_hash: str, block: Block):
    tx_traces = block.get_filtered_traces(tx_hash)
    to_address = get_tx_to_address(tx_hash, block)

    if to_address is None:
        raise ValueError("No to address found")

    addresses_to_check = []

    # check for proxies, add them to addresses to check
    proxies = get_tx_proxies(tx_traces, to_address)

    for proxy in proxies:
        addresses_to_check.append(proxy.lower())

    # check if the 'to' field is a known aggregator/router
    # if not, add to relevant addresses to run TF on
    if not is_known_router_address(to_address):
        addresses_to_check.append(
            to_address.lower()
        )  # traces need lowercase addresses to match

    ether_flows = get_ether_flows(tx_traces, addresses_to_check)
    dollar_flows = get_dollar_flows(tx_traces, addresses_to_check)
    # print(addresses_to_check)
    # print('net eth flow', ether_flows[0] - ether_flows[1])
    # print('net dollar flow', dollar_flows )
    return {"ether_flows": ether_flows, "dollar_flows": dollar_flows}


# note: not the gas set by user, only gas consumed upon execution
# def get_gas_used_by_tx(tx_hash):
#     # tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
#     return tx_receipt["gasUsed"]


# tx_traces = get_tx_traces('0x4121ce805d33e952b2e6103a5024f70c118432fd0370128d6d7845f9b2987922', 11930296)
# print(tx_traces)

# print(type(known_router_addresses))
# print(is_stablecoin_address("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"))

# run_tokenflow("0x4121ce805d33e952b2e6103a5024f70c118432fd0370128d6d7845f9b2987922", 11930296)

# delegate call test
# run_tokenflow("0x9007b339c81de366cd53539edc15c86ffc87542c65f374c0d4d1f8823a3ccf60", 12051659)

# stable flow test
# res  = run_tokenflow("0x496836e0bd1520388e36c79d587a31d4b3306e4f25352164178ca0667c7f9c29", 11935012)
# print(res)

# complex arb test
# res = run_tokenflow("0x5ab21bfba50ad3993528c2828c63e311aafe93b40ee934790e545e150cb6ca73", 11931272)
# print(res)

# get_gas_used_by_tx("0x4121ce805d33e952b2e6103a5024f70c118432fd0370128d6d7845f9b2987922")
