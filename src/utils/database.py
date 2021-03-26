from asyncpg import create_pool
from os import getenv

from loguru import logger


class Database:
    """A database interface for the bot to connect to Postgres."""

    def __init__(self):
        self.guilds = {}

    async def setup(self):
        logger.info("Setting up database...")
        self.pool = await create_pool(
            host=getenv("DB_HOST", "127.0.0.1"),
            port=getenv("DB_PORT", 5432),
            database=getenv("DB_DATABASE"),
            user=getenv("DB_USER", "root"),
            password=getenv("DB_PASS", "password"),
        )
        logger.info("Database setup complete.")

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def create_user(self, id: int):
        return await self.fetchrow("INSERT INTO Users (id) VALUES ($1) RETURNING *;", id)

    async def fetch_user(self, id: int):
        user = await self.fetchrow("SELECT * FROM Users WHERE id = $1;", id)

        if user:
            return user

        return await self.create_user(id)

    async def create_topic(self, author: int, data: str):
        await self.fetch_user(author)
        return await self.fetchrow("INSERT INTO Topics (author_id, topic) VALUES ($1, $2) RETURNING *;", author, data)

    async def delete_topic(self, id: int):
        await self.execute("DELETE FROM Topics WHERE id = $1;", id)

    async def get_random_topic(self):
        return await self.fetchrow("SELECT * FROM Topics ORDER BY RANDOM() LIMIT 1;")

    async def get_topic_by_id(self, id: int):
        return await self.fetchrow("SELECT * FROM Topics WHERE id = $1;", id)

    async def get_topics(self):
        return await self.fetch("SELECT * FROM Topics;")

    async def create_trivia_question(self, author: int, data: str, answers: str):
        await self.fetch_user(author)
        return await self.fetchrow("INSERT INTO TriviaQuestions (author_id, question, answers) VALUES ($1, $2, $3) RETURNING *;", author, data, answers)

    async def delete_trivia_question(self, id: int):
        await self.execute("DELETE FROM TriviaQuestions WHERE id = $1;", id)

    async def get_random_trivia_question(self):
        return await self.fetchrow("SELECT * FROM TriviaQuestions ORDER BY RANDOM() LIMIT 1;")

    async def get_trivia_question_by_id(self, id: int):
        return await self.fetchrow("SELECT * FROM TriviaQuestions WHERE id = $1;", id)

    async def get_trivia_questions(self):
        return await self.fetch("SELECT * FROM TriviaQuestions;")
