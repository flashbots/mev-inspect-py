from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from .swaps import Swap
from .traces import Classification, DecodedCallTrace, Protocol
from .transfers import Transfer
from .nft_trade import NftTrade


class Classifier(ABC):
    @staticmethod
    @abstractmethod
    def get_classification() -> Classification:
        raise NotImplementedError()


class TransferClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.transfer

    @staticmethod
    @abstractmethod
    def get_transfer(trace: DecodedCallTrace) -> Transfer:
        raise NotImplementedError()


class SwapClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.swap

    @staticmethod
    @abstractmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:
        raise NotImplementedError()


class LiquidationClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.liquidate


class SeizeClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.seize

class NftTradeClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.nft_trade

    @staticmethod
    @abstractmethod
    def parse_trade(
        trace: DecodedCallTrace,
        child_transfers: List[Transfer],
    ) -> Optional[NftTrade]:
        return NotImplementedError()


class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifiers: Dict[str, Type[Classifier]] = {}
