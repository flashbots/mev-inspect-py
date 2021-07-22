from mev_inspect.schemas.utils import to_original_json_dict


class Processor:
    def __init__(self, base_provider, inspectors) -> None:
        self.base_provider = base_provider
        self.inspectors = inspectors

    def get_transaction_evaluations(self, block_data):
        for transaction_hash in block_data.transaction_hashes:
            traces = block_data.get_filtered_traces(transaction_hash)
            traces_json = [to_original_json_dict(trace) for trace in traces]

            for inspector in self.inspectors:
                inspector.inspect(traces_json)
