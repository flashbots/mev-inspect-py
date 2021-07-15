from mev_inspect.schemas.utils import to_original_json_dict


class Processor:
    def __init__(self, base_provider, inspectors) -> None:
        self.base_provider = base_provider
        self.inspectors = inspectors

    def get_transaction_evaluations(self, block_data):
        for transaction_hash in block_data.transaction_hashes:
            calls = block_data.get_filtered_calls(transaction_hash)
            calls_json = [
                to_original_json_dict(call)
                for call in calls
            ]

            for inspector in self.inspectors:
                inspector.inspect(calls_json)
