from typing import Optional
from fastapi import FastAPI
from psycopg import AsyncConnection

DATABASE_URL = "postgresql://admin:admin@192.168.105.3:30317/yar"

app = FastAPI()
# database: Optional[Connection] = None
database: AsyncConnection = None

@app.on_event("startup")
async def startup():
    global database
    database = await AsyncConnection.connect(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await database.close()

@app.get('/lemmas/')
async def read_notes():
    query = 'SELECT "id", "text", "part_of_speech" FROM "lemmas"'
    async with database.cursor() as cursor:
        await cursor.execute(query)
        result = [c async for c in cursor]
    return result
