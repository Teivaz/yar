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
async def get_lemmas():
    query = 'SELECT "id", "text", "part_of_speech" FROM "lemmas"'
    async with database.cursor() as cursor:
        await cursor.execute(query)
        result = [c async for c in cursor]
    return result

@app.get('/lemma/{lemma_id}')
async def get_lemma(lemma_id: int):
    async with database.cursor() as cursor:
        await cursor.execute('SELECT "id", "text", "part_of_speech" FROM "lemmas" where "id"=%s', (lemma_id,))
        return await cursor.fetchone()

@app.get('/paradigm/{lemma_id}')
async def get_paradigm(lemma_id: int):
    result = {}
    async with database.cursor() as cursor:
        await cursor.execute('SELECT "id", "text", "part_of_speech" FROM "lemmas" where "id"=%s', (lemma_id,))
        result['lemma'] = await cursor.fetchone()
        await cursor.execute('SELECT "id", "text" FROM "word_forms" where "lemma_id"=%s', (lemma_id,))
        result['word_forms'] = [c async for c in cursor]
    return result
