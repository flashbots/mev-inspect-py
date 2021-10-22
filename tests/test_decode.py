import pydantic

from mev_inspect import decode
from mev_inspect.schemas import abi


def test_decode_function_with_simple_argument():
    test_function_name = "testFunction"
    test_parameter_name = "testParameter"
    test_abi = pydantic.parse_obj_as(
        abi.ABI,
        [
            {
                "name": test_function_name,
                "type": "function",
                "inputs": [{"name": test_parameter_name, "type": "uint256"}],
            }
        ],
    )
    # 4byte signature of the test function.
    # https://www.4byte.directory/signatures/?bytes4_signature=0x350c530b
    test_function_selector = "350c530b"
    test_function_argument = (
        "0000000000000000000000000000000000000000000000000000000000000001"
    )
    abi_decoder = decode.ABIDecoder(test_abi)
    call_data = abi_decoder.decode(
        "0x" + test_function_selector + test_function_argument
    )
    assert call_data.function_name == test_function_name
    assert call_data.function_signature == "testFunction(uint256)"
    assert call_data.inputs == {test_parameter_name: 1}


def test_decode_function_with_tuple_argument():
    test_function_name = "testFunction"
    test_tuple_name = "testTuple"
    test_parameter_name = "testParameter"
    test_abi = pydantic.parse_obj_as(
        abi.ABI,
        [
            {
                "name": test_function_name,
                "type": "function",
                "inputs": [
                    {
                        "name": test_tuple_name,
                        "type": "tuple",
                        "components": [
                            {"name": test_parameter_name, "type": "uint256"}
                        ],
                    }
                ],
            }
        ],
    )
    # 4byte signature of the test function.
    # https://www.4byte.directory/signatures/?bytes4_signature=0x98568079
    test_function_selector = "98568079"
    test_function_argument = (
        "0000000000000000000000000000000000000000000000000000000000000001"
    )
    abi_decoder = decode.ABIDecoder(test_abi)
    call_data = abi_decoder.decode(
        "0x" + test_function_selector + test_function_argument
    )
    assert call_data.function_name == test_function_name
    assert call_data.function_signature == "testFunction((uint256))"
    assert call_data.inputs == {test_tuple_name: (1,)}
