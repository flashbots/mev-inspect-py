# Internal imports
from mev_inspect import utils
from mev_inspect.config import load_config
from mev_inspect.schemas.blocks import NestedTrace, TraceType
from mev_inspect.schemas.classified_traces import Classification, ClassifiedTrace
from mev_inspect.schemas.strategy import StrategyType, Strategy, Liquidation
from mev_inspect.classifier_specs import CLASSIFIER_SPECS
from mev_inspect.trace_classifier import TraceClassifier
from mev_inspect import block

# External Libraries
import json
import pandas as pd
from typing import Optional
from web3 import Web3
from typing import List, Optional

# TODO: adjust profit to new model
#        unit test
#        coinbase check / collateral source
#
#
# Block inspect
# poetry run inspect -b 12498502 -r 'http://162.55.96.141:8546/'
#
#
#

liquidations = []
result = []

# Protocol contract address must be in included, below is AaveLendingPoolCoreV1
addrs = ['0x3dfd23A6c5E8BbcFc9581d2E864a68feb6a076d3']
from_doubles = []
transfers_to = []
transfers_from = []
# Inspect list of classified traces and identify liquidation
def find_liquidations(traces: List[ClassifiedTrace]):
    tx = []

    # For each trace
    for count, trace in enumerate(traces):

        # Check for liquidation and register trace and unique liquidator
        if (
            trace.classification == Classification.liquidate and
            trace.transaction_hash not in tx
            ):

            liquidations.append(trace)
            addrs.append(trace.from_address)
            tx.append(trace.transaction_hash)
            print(f"\nLiquidation found: \n\t{trace.from_address}")
            print(f"\nHash: \n\t{trace.transaction_hash}\n")
            print(f"\nGas Used: {trace.gas_used}\n")

            # Found liquidation, now parse inputs for data
            for i in trace.inputs:

                if(i == '_purchaseAmount'):
                    liquidation_amount = trace.inputs[i]
                elif (i == '_collateral'):
                    collateral_type = trace.inputs[i]
                    print(f"Collateral type: {collateral_type}")
                    #This will be the address of the sent token
                elif (i == '_reserve'):
                    reserve = trace.inputs[i]
                    print(f"Reserve: {reserve}")
                    #This will be the address of the received token
                elif(i == '_user'):
                    liquidated_usr = trace.inputs[i]
            # Register liquidation
            result.append(
                            Liquidation(collateral_type=collateral_type,
                                            collateral_amount=liquidation_amount,
                                            collateral_source="",
                                            reserve=reserve,
                                            strategy=StrategyType.liquidation,
                                            traces=liquidations,
                                            protocols=[trace.protocol],)
                          )

        # Check for transfer from a registered liquidator
        elif (
              trace.classification  ==  Classification.transfer and
              'sender' in trace.inputs and
              trace.inputs['sender'] in addrs and
              trace.transaction_hash not in from_doubles
             ):

            liquidator = next(addrs[i] for i in range(len(addrs)) if trace.inputs['sender'] == addrs[i])
            transfers_from.append(["from", liquidator, trace.transaction_hash, trace.inputs['amount']])
            from_doubles.append(trace.transaction_hash)

            print(f"""
                  \nTransfer from liquidator {liquidator}:
                  \n\tAmount sent: {trace.inputs['amount']} to
                  \n\t{trace.inputs['recipient']}
                  \n\tTransaction: {trace.transaction_hash}\n
                  """)

        # Check for transfer to a registered liquidator
        elif (
              trace.classification == Classification.transfer and
              trace.inputs['recipient'] in addrs
             ):

            liquidator = next(addrs[i] for i in range(len(addrs)) if trace.inputs['recipient'] == addrs[i])
            transfers_to.append(["to", liquidator, trace.transaction_hash, trace.inputs['amount']])

            print(f"""
                  \nTransfer to liquidator {liquidator}:
                  \n\tAmount in received token: {trace.inputs['amount']} from
                  \n\t{trace.from_address}
                  \n\tTransaction: {trace.transaction_hash}\n
                  """)

    for count, trace in enumerate(liquidations):
        tx = trace.transaction_hash
        #convert token to ETH
        #profit = transfers[count][2] - transfers[count+1][2]


    profits = []
    for count, trace in enumerate(transfers_to):
        profits.append({"liquidator" : transfers_to[count][1],
                        "transaction" : transfers_to[count][2],
                        "profit" : transfers_to[count][3] - transfers_from[count][3]})

    print(profits)
    print(liquidations)
    return result


rpc = 'http://162.55.96.141:8546/'
block_number = 12498502
base_provider = Web3.HTTPProvider(rpc)
block_data = block.create_from_block_number(block_number, base_provider)
trace_clasifier = TraceClassifier(CLASSIFIER_SPECS)
classified_traces = trace_clasifier.classify(block_data.traces)
fin = find_liquidations(classified_traces)
