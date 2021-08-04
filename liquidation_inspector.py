import json
from typing import Optional

from web3 import Web3

from typing import List, Optional

from mev_inspect import utils
from mev_inspect.config import load_config
from mev_inspect.schemas.blocks import NestedTrace, TraceType
from mev_inspect.schemas.classified_traces import Classification, ClassifiedTrace
from mev_inspect.schemas.strategy import StrategyType, Strategy, Liquidation
from mev_inspect.classifier_specs import CLASSIFIER_SPECS
from mev_inspect.trace_classifier import TraceClassifier
from mev_inspect import block

# poetry run inspect -b 12498502 -r 'http://162.55.96.141:8546/'
result = []

# Inspect list of classified traces and identify liquidation
def liquidations(traces: List[ClassifiedTrace]):
	event = []
	# For each trace
	for i in range(1, len(traces)):
		trace = traces[i]
		try:
			next = traces[i+1]
		except IndexError:
			break
		# Liquidation condition
		if trace.classification == Classification.liquidate:
		# Collateral data from the liquidation.
		# The inputs will differ by DEX, this is AAVE
			liquidator = trace.from_address
			prev = traces[i-1]
			#print(f"Previous: {prev.classification} from {prev.from_address} to {prev.to_address}")
			print(f"Liquidation found: {liquidator}")
			print(f"Hash: {trace.transaction_hash}")
			for i in trace.inputs:
				if(i == '_purchaseAmount'):
					liquidation_amount = trace.inputs[i]
					print(f"\tAmount: {liquidation_amount}")
				elif (i == '_collateral'):
					collateral_type = trace.inputs[i]
					print(f"\tType: {collateral_type}")
				elif (i == '_reserve'):
					reserve = trace.inputs[i]
					print(f"\tUnderlying: {reserve}")
				elif(i == '_user'):
					liquidated_usr = trace.inputs[i]
					print(f"\tLiquidated: {liquidated_usr}")
				# Define the address of the liquidator

				# Find a transfer before liquidation with a to_address corresponding to the liquidator
			for tx in traces:
				if ((tx.classification==Classification.transfer) and (tx.inputs['recipient'] == liquidator)):
					amount_received = tx.inputs['amount']
					print(f"Transfer to liquidator {liquidator}: \nAmount in received token: {tx.inputs['amount']} \nTransaction: {tx.transaction_hash}")

			# Tag liquidation
			result.append(Liquidation(strategy=StrategyType.liquidation,
									  traces=[trace, next],
									  protocols=[trace.protocol],
									  collateral_type=collateral_type,
									  collateral_amount=liquidation_amount,
									  reserve=reserve,
									  collateral_source="",))
	return result

rpc = 'http://162.55.96.141:8546/'
block_number = 12498502
base_provider = Web3.HTTPProvider(rpc)
block_data = block.create_from_block_number(block_number, base_provider)
trace_clasifier = TraceClassifier(CLASSIFIER_SPECS)
classified_traces = trace_clasifier.classify(block_data.traces)
print(liquidations(classified_traces)[2])
