from mev_inspect.schemas.classified_traces import (
    ClassifierSpec,
    Protocol,
)

"""
Deployment addresses found here
https://curve.readthedocs.io/ref-addresses.html

organized into 3 groups
1. Base Pools: 2 or more tokens implementing stable swap
  - StableSwap<pool>
  - Deposit<pool>
  - CurveContract<version>
  - CurveTokenV1/V2
2. Meta Pools: 1 token trading with an LP from above
  - StableSwap<pool>
  - Deposit<pool>
  - CurveTokenV1/V2
3. Liquidity Gauges: stake LP get curve governance token?
  - LiquidityGauge
  - LiquidityGaugeV1/V2
  - LiquidityGaugeReward
4. DAO stuff
5..? Other stuff, haven't decided if important
"""
CURVE_BASE_POOLS = [
    ClassifierSpec(
        abi_name="CurveTokenV1",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0x3B3Ac5386837Dc563660FB6a0937DFAa5924333B",  # BUSD
            "0xD905e2eaeBe188fc92179b6350807D8bd91Db0D8",  # PAX
            "0x49849C98ae39Fff122806C06791Fa73784FB3675",  # renBTC
            "0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3",  # sBTC
            "0xC25a3A3b969415c80451098fa907EC722572917F",  # sUSD
            "0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23",  # USDT
        ],
    ),
    ClassifierSpec(
        abi_name="CurveTokenV2",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",  # 3Pool
            "0xb19059ebb43466C323583928285a49f558E572Fd",  # hBTC
        ],
    ),
    ClassifierSpec(
        abi_name="CurveTokenV3",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xFd2a8fA60Abd58Efe3EeE34dd494cD491dC14900",  # AAVE
            "0xaA17A236F2bAdc98DDc0Cf999AbB47D47Fc0A6Cf",  # ankrETH
            "0x194eBd173F6cDacE046C53eACcE9B953F28411d1",  # EURS
            "0x5282a4eF67D9C33135340fB3289cc1711c13638C",  # IronBank
            "0xcee60cfa923170e4f8204ae08b4fa6a3f5656f3a",  # Link
            "0x53a901d48795C58f485cBB38df08FA96a24669D5",  # rETH
            "0x02d341CcB60fAaf662bC0554d13778015d1b285C",  # sAAVE
            "0xA3D87FffcE63B53E0d54fAa1cc983B7eB0b74A9c",  # sETH
            "0x06325440D014e39736583c165C2963BA99fAf14E",  # stETH
            "0x571FF5b7b346F706aa48d696a9a4a288e9Bb4091",  # Yv2
        ],
    ),
    ClassifierSpec(
        abi_name="CurveTokenV4",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF",  # TriCrypto
        ],
    ),
    ClassifierSpec(
        abi_name="StableSwap",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7",  # 3Pool
            "0xDeBF20617708857ebe4F679508E7b7863a8A8EeE",  # AAVE
            "0xA96A65c051bF88B4095Ee1f2451C2A9d43F53Ae2",  # ankrETH
            "0x79a8C46DeA5aDa233ABaFFD40F3A0A2B1e5A4F27",  # BUSD
            "0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56",  # Compound
            "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA",  # EURS
            "0x4CA9b3063Ec5866A4B82E437059D2C43d1be596F",  # hBTC
            "0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF",  # IronBank
            "0xf178c0b5bb7e7abf4e12a4838c7b7c5ba2c623c0",  # Link
            "0x06364f10B501e868329afBc005b3492902d6C763",  # PAX
            "0x93054188d876f558f4a66B2EF1d97d16eDf0895B",  # renBTC
            "0xF9440930043eb3997fc70e1339dBb11F341de7A8",  # rETH
            "0xEB16Ae0052ed37f479f7fe63849198Df1765a733",  # sAAVE
            "0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714",  # sBTC
            "0xc5424B857f758E906013F3555Dad202e4bdB4567",  # sETH
            "0xDC24316b9AE028F1497c275EB9192a3Ea0f67022",  # stETH
            "0xA5407eAE9Ba41422680e2e00537571bcC53efBfD",  # sUSD
            "0x52EA46506B9CC5Ef470C5bf89f17Dc28bB35D85C",  # USDT
            "0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51",  # Y
            "0x8925D9d9B4569D737a48499DeF3f67BaA5a144b9",  # Yv2
        ],
    ),
    ClassifierSpec(
        abi_name="Deposit",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xb6c057591E073249F2D9D88Ba59a46CFC9B59EdB",  # BUSD
            "0xeB21209ae4C2c9FF2a86ACA31E123764A3B6Bc06",  # Compound
            "0xA50cCc70b6a011CffDdf45057E39679379187287",  # PAX
            "0xFCBa3E75865d2d561BE8D220616520c171F12851",  # sUSD
            "0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",  # TriCrypto
            "0xac795D2c97e60DF6a99ff1c814727302fD747a80",  # USDT
            "0xbBC81d23Ea2c3ec7e56D39296F0cbB648873a5d3",  # Y
        ],
    ),
]

CLASSIFIER_SPECS = [*CURVE_BASE_POOLS]
