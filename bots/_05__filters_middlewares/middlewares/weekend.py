from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


def _is_weekend() -> bool:
    # 5 - Saturday, 6 - Sunday
    return datetime.utcnow().weekday() in (5, 6)


class WeekendMessageMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        # If today is not Saturday or Sunday, then we continue processing.
        if not _is_weekend():
            return await handler(event, data)
        # Otherwise it will simply return None  and processing will stop


# This will be an outer-middleware for any callbacks
class WeekendCallbackMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]], event: CallbackQuery,
                       data: Dict[str, Any]) -> Any:
        # If today is not Saturday or Sunday, then we continue processing.
        if not _is_weekend():
            return await handler(event, data)
        # Otherwise, we respond to the callback ourselves and stop further processing
        await event.answer(
            "The bot doesn't work on weekends!",
            show_alert=True
        )
        return
