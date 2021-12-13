import asyncio
import logging
import traceback
from asyncio import CancelledError
from typing import Optional

from sqlalchemy import orm
from web3 import Web3
from web3.eth import AsyncEth

from mev_inspect.block import create_from_block_number
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.inspect_block import inspect_block
from mev_inspect.provider import get_base_provider
from mev_inspect.utils import RPCType

logger = logging.getLogger(__name__)


class MEVInspector:
    def __init__(
        self,
        rpc: str,
        inspect_db_session: orm.Session,
        trace_db_session: Optional[orm.Session],
        type: RPCType = RPCType.parity,
        max_concurrency: int = 1,
        request_timeout: int = 300,
    ):
        self.inspect_db_session = inspect_db_session
        self.trace_db_session = trace_db_session
        self.base_provider = get_base_provider(rpc, request_timeout, type)
        self.type = type
        self.w3 = Web3(self.base_provider, modules={"eth": (AsyncEth,)}, middlewares=[])
        self.trace_classifier = TraceClassifier()
        self.max_concurrency = asyncio.Semaphore(max_concurrency)

    async def create_from_block(self, block_number: int):
        return await create_from_block_number(
            base_provider=self.base_provider,
            w3=self.w3,
            type=self.type,
            block_number=block_number,
            trace_db_session=self.trace_db_session,
        )

    async def inspect_single_block(self, block: int):
        return await inspect_block(
            self.inspect_db_session,
            self.base_provider,
            self.w3,
            self.type,
            self.trace_classifier,
            block,
            trace_db_session=self.trace_db_session,
        )

    async def inspect_many_blocks(self, after_block: int, before_block: int):
        tasks = []
        for block_number in range(after_block, before_block):
            tasks.append(
                asyncio.ensure_future(
                    self.safe_inspect_block(block_number=block_number)
                )
            )
        logger.info(f"Gathered {len(tasks)} blocks to inspect")
        try:
            await asyncio.gather(*tasks)
        except CancelledError:
            logger.info("Requested to exit, cleaning up...")
        except Exception as e:
            logger.error(f"Existed due to {type(e)}")
            traceback.print_exc()

    async def safe_inspect_block(self, block_number: int):
        async with self.max_concurrency:
            return await inspect_block(
                self.inspect_db_session,
                self.base_provider,
                self.w3,
                self.type,
                self.trace_classifier,
                block_number,
                trace_db_session=self.trace_db_session,
            )
