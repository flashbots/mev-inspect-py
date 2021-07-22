from typing import List

from hexbytes.main import HexBytes


def check_trace_for_signature(trace: dict, signatures: List[str]):
    if trace["action"]["input"] == None:
        return False

    ## Iterate over all signatures, and if our trace matches any of them set it to True
    for signature in signatures:
        if HexBytes(trace["action"]["input"]).startswith(signature):
            ## Note that we are turning the input into hex bytes here, which seems to be fine
            ## Working with strings was doing weird things
            return True

    return False
