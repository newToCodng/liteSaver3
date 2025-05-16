from app.models.userModel import UserRegister, UserLogin, UserOut
from app.database.connection import db
import asyncpg
from app.core.security import hash_password, verify_password
from app.core.token import create_user_token
from app.core.exceptions import DatabaseError, UserAlreadyExists, InvalidLoginDetails, UserNotFound



async def create_user(user: UserRegister):
    query = """
        INSERT INTO users (email, first_name, last_name, password_hash, phone_number, dob, phone_verified)
        VALUES ($1, $2, $3, $4, $5, $6, FALSE)
        RETURNING user_id;
    """
    try:
        pwd_hash = hash_password(user.password)
        pool = db.get_pool()
        async with pool.acquire() as conn:
            user_id = await conn.fetchval(query, user.email, user.first_name, user.last_name, pwd_hash, user.phone_number, user.dob)
            return user_id
    except asyncpg.UniqueViolationError as e:
        raise UserAlreadyExists(f"User already exists: {str(e)}")
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")


async def authenticate_user(user: UserLogin):
    query = """
        SELECT user_id, email, password_hash FROM users
        WHERE email = $1;
    """

    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, user.email)
            if row is None:
                raise InvalidLoginDetails("Invalid email or password")

            if not verify_password(user.password, row["password_hash"]):
                raise InvalidLoginDetails("Invalid email or password")

            token_data = {"sub": row["email"], "user_id": row["user_id"]}
            access_token = create_user_token(token_data)
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Login successful ✅"
            }
    except InvalidLoginDetails:
        raise  # pass on to the router
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Authentication error occurred: {str(e)}")


async def get_user_profile(user_id: int) -> UserOut:
    query = """
        SELECT user_id, email, first_name, last_name
        FROM users
        WHERE user_id = $1;
    """

    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            if row is None:
                raise UserNotFound(f"User with id {user_id} not found")

            return UserOut(
                user_id=row["user_id"],
                email=row["email"],
                first_name=row["first_name"],
                last_name=row["last_name"]
            )
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")
