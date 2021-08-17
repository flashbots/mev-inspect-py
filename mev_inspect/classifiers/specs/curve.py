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
        abi_name="StableSwap3Pool",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"],
    ),
    ClassifierSpec(
        abi_name="StableSwapAAVE",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xDeBF20617708857ebe4F679508E7b7863a8A8EeE"],
    ),
    ClassifierSpec(
        abi_name="StableSwapAETH",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xA96A65c051bF88B4095Ee1f2451C2A9d43F53Ae2"],
    ),
    ClassifierSpec(
        abi_name="StableSwapBUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x79a8C46DeA5aDa233ABaFFD40F3A0A2B1e5A4F27"],
    ),
    ClassifierSpec(
        abi_name="StableSwapCompound",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56"],
    ),
    ClassifierSpec(
        abi_name="StableSwapEURS",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x0Ce6a5fF5217e38315f87032CF90686C96627CAA"],
    ),
    ClassifierSpec(
        abi_name="StableSwaphBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x4CA9b3063Ec5866A4B82E437059D2C43d1be596F"],
    ),
    ClassifierSpec(
        abi_name="StableSwapIronBank",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF"],
    ),
    ClassifierSpec(
        abi_name="StableSwapLink",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xf178c0b5bb7e7abf4e12a4838c7b7c5ba2c623c0"],
    ),
    ClassifierSpec(
        abi_name="StableSwapPAX",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x06364f10B501e868329afBc005b3492902d6C763"],
    ),
    ClassifierSpec(
        abi_name="StableSwaprenBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x93054188d876f558f4a66B2EF1d97d16eDf0895B"],
    ),
    ClassifierSpec(
        abi_name="StableSwaprETH",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xF9440930043eb3997fc70e1339dBb11F341de7A8"],
    ),
    ClassifierSpec(
        abi_name="StableSwapsAAVE",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xEB16Ae0052ed37f479f7fe63849198Df1765a733"],
    ),
    ClassifierSpec(
        abi_name="StableSwapsBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714"],
    ),
    ClassifierSpec(
        abi_name="StableSwapsETH",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xc5424B857f758E906013F3555Dad202e4bdB4567"],
    ),
    ClassifierSpec(
        abi_name="StableSwapstETH",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xDC24316b9AE028F1497c275EB9192a3Ea0f67022"],
    ),
    ClassifierSpec(
        abi_name="StableSwapsUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xA5407eAE9Ba41422680e2e00537571bcC53efBfD"],
    ),
    ClassifierSpec(
        abi_name="StableSwapUSDT",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x52EA46506B9CC5Ef470C5bf89f17Dc28bB35D85C"],
    ),
    ClassifierSpec(
        abi_name="StableSwapY",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51"],
    ),
    ClassifierSpec(
        abi_name="StableSwapYv2",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x8925D9d9B4569D737a48499DeF3f67BaA5a144b9"],
    ),
    ClassifierSpec(
        abi_name="DepositBUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xb6c057591E073249F2D9D88Ba59a46CFC9B59EdB"],
    ),
    ClassifierSpec(
        abi_name="DepositCompound",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xeB21209ae4C2c9FF2a86ACA31E123764A3B6Bc06"],
    ),
    ClassifierSpec(
        abi_name="DepositPAX",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xA50cCc70b6a011CffDdf45057E39679379187287"],
    ),
    ClassifierSpec(
        abi_name="DepositsUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xFCBa3E75865d2d561BE8D220616520c171F12851"],
    ),
    ClassifierSpec(
        abi_name="DepositTriCrypto",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785"],
    ),
    ClassifierSpec(
        abi_name="DepositUSDT",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xac795D2c97e60DF6a99ff1c814727302fD747a80"],
    ),
    ClassifierSpec(
        abi_name="DepositY",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xbBC81d23Ea2c3ec7e56D39296F0cbB648873a5d3"],
    ),
]

CURVE_META_POOLS = [
    ClassifierSpec(
        abi_name="CurveTokenV2",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0x3a664Ab939FD8482048609f652f9a0B0677337B9",  # DUSD
            "0xD2967f45c4f384DEEa880F807Be904762a3DeA07",  # GUSD
            "0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858",  # HUSD
            "0x6D65b498cb23deAba52db31c93Da9BFFb340FB8F",  # LinkUSD
            "0x1AEf73d49Dedc4b1778d0706583995958Dc862e6",  # MUSD
            "0xDE5331AC4B3630f94853Ff322B66407e0D6331E8",  # pBTC
            "0xC2Ee6b0334C261ED60C72f6054450b61B8f18E35",  # RSV
            "0x64eda51d3Ad40D56b9dFc5554E06F94e1Dd786Fd",  # tBTC
            "0x97E2768e8E73511cA874545DC5Ff8067eB19B787",  # USDK
            "0x4f3E8F405CF5aFC05D68142F3783bDfE13811522",  # USDN
        ],
    ),
    ClassifierSpec(
        abi_name="CurveTokenV3",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0x410e3E86ef427e30B9235497143881f717d93c2A",  # bBTC
            "0x2fE94ea3d5d4a175184081439753DE15AeF9d614",  # oBTC
            "0x7Eb40E450b9655f4B3cC4259BCC731c63ff55ae6",  # USDP
            "0x7Eb40E450b9655f4B3cC4259BCC731c63ff55ae6",  # UST
        ],
    ),
    ClassifierSpec(
        abi_name="DepositbBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xC45b2EEe6e09cA176Ca3bB5f7eEe7C47bF93c756"],
    ),
    ClassifierSpec(
        abi_name="DepositDUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x61E10659fe3aa93d036d099405224E4Ac24996d0"],
    ),
    ClassifierSpec(
        abi_name="DepositGUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x64448B78561690B70E17CBE8029a3e5c1bB7136e"],
    ),
    ClassifierSpec(
        abi_name="DepositHUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x09672362833d8f703D5395ef3252D4Bfa51c15ca"],
    ),
    ClassifierSpec(
        abi_name="DepositLinkUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x1de7f0866e2c4adAC7b457c58Cc25c8688CDa1f2"],
    ),
    ClassifierSpec(
        abi_name="DepositMUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x803A2B40c5a9BB2B86DD630B274Fa2A9202874C2"],
    ),
    ClassifierSpec(
        abi_name="DepositoBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xd5BCf53e2C81e1991570f33Fa881c49EEa570C8D"],
    ),
    ClassifierSpec(
        abi_name="DepositpBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x11F419AdAbbFF8d595E7d5b223eee3863Bb3902C"],
    ),
    ClassifierSpec(
        abi_name="DepositRSV",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xBE175115BF33E12348ff77CcfEE4726866A0Fbd5"],
    ),
    ClassifierSpec(
        abi_name="DeposittBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xaa82ca713D94bBA7A89CEAB55314F9EfFEdDc78c"],
    ),
    ClassifierSpec(
        abi_name="DepositUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xF1f85a74AD6c64315F85af52d3d46bF715236ADc",
            "0x094d12e5b541784701FD8d65F11fc0598FBC6332"
            "0x3c8cAee4E09296800f8D29A68Fa3837e2dae4940",
        ],
    ),
    ClassifierSpec(
        abi_name="DepositUST",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xB0a0716841F2Fc03fbA72A891B8Bb13584F52F2d"],
    ),
    ClassifierSpec(
        abi_name="StableSwapbBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x071c661B4DeefB59E2a3DdB20Db036821eeE8F4b"],
    ),
    ClassifierSpec(
        abi_name="StableSwapDUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x8038C01A0390a8c547446a0b2c18fc9aEFEcc10c"],
    ),
    ClassifierSpec(
        abi_name="StableSwapGUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x4f062658EaAF2C1ccf8C8e36D6824CDf41167956"],
    ),
    ClassifierSpec(
        abi_name="StableSwapHUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x3eF6A01A0f81D6046290f3e2A8c5b843e738E604"],
    ),
    ClassifierSpec(
        abi_name="StableSwapLinkUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171"],
    ),
    ClassifierSpec(
        abi_name="StableSwapMUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x8474DdbE98F5aA3179B3B3F5942D724aFcdec9f6"],
    ),
    ClassifierSpec(
        abi_name="StableSwapoBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xd81dA8D904b52208541Bade1bD6595D8a251F8dd"],
    ),
    ClassifierSpec(
        abi_name="StableSwappBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x7F55DDe206dbAD629C080068923b36fe9D6bDBeF"],
    ),
    ClassifierSpec(
        abi_name="StableSwapRSV",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xC18cC39da8b11dA8c3541C598eE022258F9744da"],
    ),
    ClassifierSpec(
        abi_name="StableSwaptBTC",
        protocol=Protocol.curve,
        valid_contract_addresses=["0xC25099792E9349C7DD09759744ea681C7de2cb66"],
    ),
    ClassifierSpec(
        abi_name="StableSwapUSD",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0x3E01dD8a5E1fb3481F0F589056b428Fc308AF0Fb",
            "0x0f9cb53Ebe405d49A0bbdBD291A65Ff571bC83e1",
        ],
    ),
    ClassifierSpec(
        abi_name="StableSwapUSDP",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x42d7025938bEc20B69cBae5A77421082407f053A"],
    ),
    ClassifierSpec(
        abi_name="StableSwapUST",
        protocol=Protocol.curve,
        valid_contract_addresses=["0x890f4e345B1dAED0367A877a1612f86A1f86985f"],
    ),
]

"""
CURVE_LIQUIDITY_GAUGES = [
    ClassifierSpec(
        abi_name="LiquidityGauge",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A",  # 3Pool
            "0x69Fb7c45726cfE2baDeE8317005d3F94bE838840",  # BUSD
            "0x7ca5b0a2910B33e9759DC7dDB0413949071D7575",  # Compound
            "0xC5cfaDA84E902aD92DD40194f0883ad49639b023",  # GUSD
            "0x4c18E409Dc8619bFb6a1cB56D114C3f592E0aE79",  # hBTC
            "0x2db0E83599a91b508Ac268a6197b8B14F5e72840",  # HUSD
            "0x64E3C23bfc40722d3B649844055F1D51c1ac041d",  # PAX
            "0xB1F2cdeC61db658F091671F5f199635aEF202CAC",  # renBTC
            "0xC2b1DF84112619D190193E48148000e3990Bf627",  # USDK
            "0xF98450B5602fa59CC66e1379DFfB6FDDc724CfC4",  # USDN
            "0xBC89cd85491d81C6AD2954E6d0362Ee29fCa8F53",  # USDT
            "0xFA712EE4788C042e2B7BB55E6cb8ec569C4530c1",  # Y
        ],
    ),
    ClassifierSpec(
        abi_name="LiquidityGaugeV2",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xd662908ADA2Ea1916B3318327A97eB18aD588b5d",  # AAVE
            "0x6d10ed2cF043E6fcf51A0e7b4C2Af3Fa06695707",  # ankrETH
            "0xdFc7AdFa664b08767b735dE28f9E84cd30492aeE",  # bBTC
            "0x90Bb609649E0451E5aD952683D64BD2d1f245840",  # EURS
            "0x72e158d38dbd50a483501c24f792bdaaa3e7d55c",  # FRAX
            "0x11137B10C210b579405c21A07489e28F3c040AB1",  # oBTC
            "0xF5194c3325202F456c95c1Cf0cA36f8475C1949F",  # IronBank
            "0xFD4D8a17df4C27c1dD245d153ccf4499e806C87D",  # Link
            "0xd7d147c6Bb90A718c3De8C0568F9B560C79fa416",  # pBTC
            "0x462253b8F74B72304c145DB0e4Eebd326B22ca39",  # sAAVE
            "0x3C0FFFF15EA30C35d7A85B85c0782D6c94e1d238",  # sETH
            "0x182B723a58739a9c974cFDB385ceaDb237453c28",  # stETH
            "0x055be5DDB7A925BfEF3417FC157f53CA77cA7222",  # USDP
            "0x3B7020743Bc2A4ca9EaF9D0722d42E20d6935855",  # UST
            "0x8101E6760130be2C8Ace79643AB73500571b7162",  # Yv2
        ],
    ),
    ClassifierSpec(
        abi_name="LiquidityGaugeV3",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0x9582C4ADACB3BCE56Fea3e590F05c3ca2fb9C477",  # alUSD
            "0x824F13f1a2F29cFEEa81154b46C0fc820677A637",  # rETH
            "0x6955a55416a06839309018A8B0cB72c4DDC11f15",  # TriCrypto
        ],
    ),
    ClassifierSpec(
        abi_name="LiquidityGaugeReward",
        protocol=Protocol.curve,
        valid_contract_addresses=[
            "0xAEA6c312f4b3E04D752946d329693F7293bC2e6D",  # DUSD
            "0x5f626c30EC1215f4EdCc9982265E8b1F411D1352",  # MUSD
            "0x4dC4A289a8E33600D8bD4cf5F6313E43a37adec7",  # RSV
            "0x705350c4BcD35c9441419DdD5d2f097d7a55410F",  # sBTC
            "0xA90996896660DEcC6E997655E065b23788857849",  # sUSDv2
            "0x6828bcF74279eE32f2723eC536c22c51Eed383C6",  # tBTC
        ],
    ),
]
"""

CURVE_CLASSIFIER_SPECS = [*CURVE_BASE_POOLS, *CURVE_META_POOLS]
