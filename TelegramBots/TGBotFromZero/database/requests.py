from database.models import async_session
from database.models import User
from sqlalchemy import select

async def add_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, name=username))  
            await session.commit()  


