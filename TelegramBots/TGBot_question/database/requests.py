from sqlalchemy import select, update, delete
from database.models import async_session, User, QuestionSession
from sqlalchemy.exc import SQLAlchemyError

# Добавление нового пользователя
async def add_new_user(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        if not user:
            session.add(User(tg_id = user_id))
            await session.commit()
            return False
        else:
            return True

# Обновление данных пользователя
async def update_user_data(name, chanell_link, user_id):
    try:
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == user_id))
            if user:
                user.name = name
                user.chanell_link = chanell_link
                await session.commit()
            else:
                print(f"User with tg_id={user_id} not found!")
    except SQLAlchemyError as e:
        print(f"Error updating user data: {e}")

# Сохранение связи между пользователями (Пользователь Б и Пользователь А)
async def save_target_user_id(user_id, target_user_id):
    try:
        async with async_session() as session:
            session.add(QuestionSession(user_b_id=user_id, user_a_id=target_user_id))
            await session.commit()
    except SQLAlchemyError as e:
        print(f"Error saving target user ID: {e}")

async def get_target_user_id(user_id):
    async with async_session() as session:
        return await session.scalar(
            select(QuestionSession.user_a_id)
            .where(QuestionSession.user_b_id == user_id)
            .order_by(QuestionSession.id.desc())
        )