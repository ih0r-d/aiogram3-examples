from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message


class HasUsernamesFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        # If there are no entities at all, None will be returned,
        # in this case we assume that this is an empty list
        entities = message.entities or []

        # Check any usernames and extract them from the text
        # using the extract_from() method. For more details, see chapter
        # about working with messages
        found_usernames = [
            item.extract_from(message.text) for item in entities
            if item.type == "mention"
        ]

        # If there are usernames, then we “push” them into the handler
        # by "usernames"
        if len(found_usernames) > 0:
            return {"user_names": found_usernames}
        # If we didn't find any usernames, return False
        return False
