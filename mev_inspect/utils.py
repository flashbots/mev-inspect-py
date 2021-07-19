from hexbytes.main import HexBytes


def check_call_for_signature(call, signatures):
    if call["action"]["input"] == None:
        return False

    ## By default set this to False
    signature_present_boolean = False

    ## Iterate over all signatures, and if our call matches any of them set it to True
    for signature in signatures:
        # print("Desired signature:", str(signature))
        # print("Actual", HexBytes(call['action']['input']))

        if HexBytes(call["action"]["input"]).startswith((signature)):
            ## Note that we are turning the input into hex bytes here, which seems to be fine
            ## Working with strings was doing weird things
            print("hit")
            signature_present_boolean = True

    return signature_present_boolean
