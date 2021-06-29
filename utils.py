
def check_call_for_signature(call, signatures):
    if (call.action.input == None):
        return False
    
    ## By default set this to False
    signature_present_boolean = False

    ## Iterate over all signatures, and if our call matches any of them set it to True
    for signature in signatures:
        if call.action.input.startsWith(signature):
            signature_present_boolean = True

    return signature_present_boolean