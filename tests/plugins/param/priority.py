from typing import Optional

from nonebot.adapters import Bot, Event, Message
from nonebot.matcher import Matcher
from nonebot.params import Arg, Depends
from nonebot.typing import T_State


def dependency():
    return 1


async def complex_priority(
    sub: int = Depends(dependency),
    bot: Optional[Bot] = None,
    event: Optional[Event] = None,
    state: T_State = {},
    matcher: Optional[Matcher] = None,
    arg: Message = Arg(),
    exception: Optional[Exception] = None,
    default: int = 1,
): ...
