from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.user import UserLogin
from app.core.security import verify_password


async def user_exists(db: AsyncSession, email: str) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() is not None

async def create_user(user: UserCreate, db: AsyncSession) -> User:
    if await user_exists(db, user.email):
        raise ValueError("User with this email already exists")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def user_login(user: UserLogin, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(
        (User.email == user.username_or_email) | (User.username == user.username_or_email)
    ))
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        raise ValueError("No user found with this email or username")
    if not verify_password(user.password, existing_user.hashed_password):
        raise ValueError("Invalid email or password")
    return existing_user