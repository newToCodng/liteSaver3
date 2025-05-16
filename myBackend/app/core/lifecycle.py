from app.database.connection import db


async def startup():
    return await db.connect()


async def shutdown():
    return await db.disconnect()
