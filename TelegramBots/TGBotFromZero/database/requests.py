from database.models import async_session
from database.models import User
from sqlalchemy import select

async def add_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, username=username))  
            await session.commit()  

async def view_all_user():
    async with async_session() as session:
        all_user = await session.scalars(select(User))
        return all_user.all()

