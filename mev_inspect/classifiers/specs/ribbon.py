from mev_inspect.schemas.classified_traces import Protocol
from mev_inspect.schemas.classifiers import ClassifierSpec


RIBBON_VAULT_ADDRESSES = [
    "0x65a833afDc250D9d38f8CD9bC2B1E3132dB13B2F",
    "0x0FABaF48Bbf864a3947bdd0Ba9d764791a60467A",
    "0x8b5876f5B0Bf64056A89Aa7e97511644758c3E8c",
    "0x16772a7f4a3ca291C21B8AcE76F9332dDFfbb5Ef",
    "0x8FE74471F198E426e96bE65f40EeD1F8BA96e54f",
    "0x25751853Eab4D0eB3652B5eB6ecB102A2789644B",
]


RIBBON_VAULT_SPEC = ClassifierSpec(
    abi_name="RibbonThetaVault",
    protocol=Protocol.ribbon,
    valid_contract_address=RIBBON_VAULT_ADDRESSES,
)
