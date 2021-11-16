from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from .traces import Classification, DecodedCallTrace, Protocol
from .transfers import Transfer
from .punk_bid import Punk_Bid
from .punk_accept_bid import Punk_Accept_Bid


class Classifier(ABC):
    @staticmethod
    @abstractmethod
    def get_classification() -> Classification:
        raise NotImplementedError()


class PunkBidClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.punk_bid

    @staticmethod
    @abstractmethod
    def get_bid(trace: DecodedCallTrace) -> Punk_Bid:
        raise NotImplementedError()


class PunkAcceptBidClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.punk_accept_bid

    @staticmethod
    @abstractmethod
    def get_accept_bid(trace: DecodedCallTrace) -> Punk_Accept_Bid:
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
    def get_swap_recipient(trace: DecodedCallTrace) -> str:
        raise NotImplementedError()


class LiquidationClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.liquidate


class SeizeClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.seize


class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifiers: Dict[str, Type[Classifier]] = {}
