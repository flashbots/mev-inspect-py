# mev-inspect-py
MEV-inspect-py is a script which "inspects" an Ethereum block, or range of blocks, and tries to identify and analyze transactions which extract MEV. For example, it will identify and quantify arbitrage trades which capture profit from mispricing across two DEXes in a single transaction.

MEV-inspect-py is currently a work in progress that builds on the work done in [MEV-inspect-rs](https://github.com/flashbots/mev-inspect-rs). In the coming weeks we will release a foundation from which contributors can add new inspectors.
