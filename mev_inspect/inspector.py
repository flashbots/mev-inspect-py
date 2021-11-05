import asyncio
import logging
import sys
import traceback
from asyncio import CancelledError

from web3 import Web3
from web3.eth import AsyncEth

from mev_inspect.block import create_from_block_number
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.db import get_inspect_sessionmaker, get_trace_sessionmaker
from mev_inspect.inspect_block import inspect_block
from mev_inspect.provider import get_base_provider

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class MEVInspector:
    def __init__(
        self,
        rpc: str,
        max_concurrency: int = 1,
        request_timeout: int = 300,
    ):
        self.base_provider = get_base_provider(rpc, request_timeout=request_timeout)
        self.w3 = Web3(self.base_provider, modules={"eth": (AsyncEth,)}, middlewares=[])
        self.trace_classifier = TraceClassifier()
        self.max_concurrency = asyncio.Semaphore(max_concurrency)

    async def create_from_block(self, block_number: int):
        trace_db_sessionmaker = await get_trace_sessionmaker()
        trace_db_session = (
            trace_db_sessionmaker() if trace_db_sessionmaker is not None else None
        )

        return await create_from_block_number(
            base_provider=self.base_provider,
            w3=self.w3,
            block_number=block_number,
            trace_db_session=trace_db_session,
        )

        if trace_db_session is not None:
            await trace_db_session.close()

    async def inspect_single_block(self, block: int):
        inspect_db_sessionmaker = await get_inspect_sessionmaker()
        trace_db_sessionmaker = await get_trace_sessionmaker()

        inspect_db_session = inspect_db_sessionmaker()
        trace_db_session = (
            trace_db_sessionmaker() if trace_db_sessionmaker is not None else None
        )

        await inspect_block(
            inspect_db_session,
            self.base_provider,
            self.w3,
            self.trace_classifier,
            block,
            trace_db_session=trace_db_session,
        )

        await inspect_db_session.close()
        if trace_db_session is not None:
            await trace_db_session.close()

    async def inspect_many_blocks(self, after_block: int, before_block: int):
        inspect_db_sessionmaker = get_inspect_sessionmaker()
        trace_db_sessionmaker = get_trace_sessionmaker()

        tasks = []

        for block_number in range(after_block, before_block):
            tasks.append(
                asyncio.ensure_future(
                    self.safe_inspect_block(
                        inspect_db_sessionmaker,
                        block_number,
                        trace_db_sessionmaker,
                    )
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

    async def safe_inspect_block(
        self,
        inspect_db_sessionmaker,
        block_number: int,
        trace_db_sessionmaker,
    ):
        async with self.max_concurrency:
            inspect_db_session = inspect_db_sessionmaker()
            trace_db_session = (
                trace_db_sessionmaker() if trace_db_sessionmaker is not None else None
            )

            await inspect_block(
                inspect_db_session,
                self.base_provider,
                self.w3,
                self.trace_classifier,
                block_number,
                trace_db_session=trace_db_session,
            )

            await inspect_db_session.close()
            if trace_db_session is not None:
                await trace_db_session.close()
