from mev_inspect.schemas.classifiers import ClassifierSpec
from mev_inspect.schemas.traces import Protocol

LIDO_CLASSIFIER_SPECS = [
    ClassifierSpec(
        abi_name="LidoDao",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0xb8FFC3Cd6e7Cf5a098A1c92F48009765B24088Dc"  # lido dao
        ],
    ),
    ClassifierSpec(
        abi_name="LDO",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"  # LDO token
        ],
    ),
    ClassifierSpec(
        abi_name="LidostETH",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",  # lido and stETH token
        ],
    ),
    ClassifierSpec(
        abi_name="nodeoperators",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0x55032650b14df07b85bF18A3a3eC8E0Af2e028d5"  # node operators registry
        ],
    ),
    ClassifierSpec(
        abi_name="oracle",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0x442af784A788A5bd6F42A01Ebe9F287a871243fb"  # oracle
        ],
    ),
    ClassifierSpec(
        abi_name="WstETH",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0"  # WstETH
        ],
    ),
    ClassifierSpec(
        abi_name="depositsecurity",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0xDb149235B6F40dC08810AA69869783Be101790e7"  # deposit security module
        ],
    ),
    ClassifierSpec(
        abi_name="aragonvoting",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0x2e59A20f205bB85a89C53f1936454680651E618e"  # aragon voting
        ],
    ),
    ClassifierSpec(
        abi_name="aragontokenmanager",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0xf73a1260d222f447210581DDf212D915c09a3249"  # aragon token manager
        ],
    ),
    ClassifierSpec(
        abi_name="aragonfinance",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0xB9E5CBB9CA5b0d659238807E84D0176930753d86"  # aragon finance
        ],
    ),
    ClassifierSpec(
        abi_name="aragonagent",
        protocol=Protocol.lido,
        valid_contract_addresses=[
            "0x3e40D73EB977Dc6a537aF587D48316feE66E9C8c"  # aragon agent
        ],
    ),
]
