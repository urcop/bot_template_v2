from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker

from bot.schemas.user import User


class RegisterCheck(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data['session']
        user: User = await User.get_user(
            user_id=event.from_user.id,
            session_maker=session_maker
        )

        if user is None:
            await User.add_user(
                user_id=event.from_user.id,
                full_name=event.from_user.full_name,
                username=event.from_user.username,
                session_maker=session_maker
            )

        return await handler(event, data)
