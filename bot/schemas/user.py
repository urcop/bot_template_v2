from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DATE, select, Result, insert
from sqlalchemy.orm import sessionmaker

from bot.services.db.db_base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, primary_key=True)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=True, default='Anonymous')
    reg_date = Column(DATE, default=datetime.today())
    upd_date = Column(DATE, onupdate=datetime.today())

    def __str__(self):
        return f'<User {self.user_id} - {self.username}>'

    @classmethod
    async def get_user(cls, user_id: int, session_maker: sessionmaker):
        async with session_maker as session:
            sql = select(cls).where(cls.user_id == user_id)
            result: Result = await session.execute(sql)
            return result.first()

    @classmethod
    async def add_user(cls,
                       user_id: int,
                       username: str,
                       full_name: str,
                       session_maker: sessionmaker
                       ) -> None:
        async with session_maker as session:
            sql = insert(cls).values(
                user_id=user_id,
                username=username,
                full_name=full_name
            )
            await session.execute(sql)
            await session.commit()
