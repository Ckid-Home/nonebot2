from collections.abc import Awaitable
from typing_extensions import TypeAlias
from typing import Any, Union, Callable, cast

from nonebot.utils import run_sync, is_coroutine_callable

SYNC_LIFESPAN_FUNC: TypeAlias = Callable[[], Any]
ASYNC_LIFESPAN_FUNC: TypeAlias = Callable[[], Awaitable[Any]]
LIFESPAN_FUNC: TypeAlias = Union[SYNC_LIFESPAN_FUNC, ASYNC_LIFESPAN_FUNC]


class Lifespan:
    def __init__(self) -> None:
        self._startup_funcs: list[LIFESPAN_FUNC] = []
        self._ready_funcs: list[LIFESPAN_FUNC] = []
        self._shutdown_funcs: list[LIFESPAN_FUNC] = []

    def on_startup(self, func: LIFESPAN_FUNC) -> LIFESPAN_FUNC:
        self._startup_funcs.append(func)
        return func

    def on_shutdown(self, func: LIFESPAN_FUNC) -> LIFESPAN_FUNC:
        self._shutdown_funcs.append(func)
        return func

    def on_ready(self, func: LIFESPAN_FUNC) -> LIFESPAN_FUNC:
        self._ready_funcs.append(func)
        return func

    @staticmethod
    async def _run_lifespan_func(
        funcs: list[LIFESPAN_FUNC],
    ) -> None:
        for func in funcs:
            if is_coroutine_callable(func):
                await cast(ASYNC_LIFESPAN_FUNC, func)()
            else:
                await run_sync(cast(SYNC_LIFESPAN_FUNC, func))()

    async def startup(self) -> None:
        if self._startup_funcs:
            await self._run_lifespan_func(self._startup_funcs)

        if self._ready_funcs:
            await self._run_lifespan_func(self._ready_funcs)

    async def shutdown(self) -> None:
        if self._shutdown_funcs:
            await self._run_lifespan_func(self._shutdown_funcs)

    async def __aenter__(self) -> None:
        await self.startup()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.shutdown()
