from discord.ext import commands
from discord import Intents, Message, Embed

from loguru import logger
from traceback import format_exc
from datetime import datetime
from aiohttp import ClientSession
from os import getenv

from .help import Help
from .context import Context

from src.utils.database import Database


class Bot(commands.Bot):
    """A subclass of commands.Bot with additional functionality."""

    def __init__(self, *args, **kwargs):
        logger.info("Starting up...")

        intents = Intents.all()

        super().__init__(
            command_prefix=".",
            intents=intents,
            help_command=Help(),
            *args,
            **kwargs
        )

        self.db: Database = Database()
        self.sess: ClientSession = None

    def load_extensions(self, *exts) -> None:
        """Load a given set of extensions."""

        logger.info(f"Starting loading {len(exts)} cogs...")

        success = 0

        for ext in exts:
            try:
                self.load_extension(ext)
            except:
                logger.error(f"Error while loading {ext}:\n{format_exc()}")
            else:
                logger.info(f"Successfully loaded cog {ext}.")
                success += 1

        logger.info(f"Cog loading finished. Success: {success}. Failed: {len(exts) - success}.")

    async def login(self, *args, **kwargs) -> None:
        """Create the database connection before login."""
        logger.info("Logging in to Discord...")

        await self.db.setup()

        self.sess = ClientSession()

        await super().login(*args, **kwargs)

    async def get_context(self, message: Message):
        """Get the context with the custom context class."""

        return await super().get_context(message, cls=Context)

    async def on_connect(self):
        """Log the connect event."""

        logger.info("Connected to Discord.")

    async def on_ready(self):
        await self.log(f"Connected to Discord as {self.user}")

    async def log(self, message: str, title: str = "Logging", colour: int = 0x87CEEB):
        embed = Embed(
            title=title,
            colour=colour,
            description=message,
            timestamp=datetime.utcnow(),
        )

        embed.set_footer(
            text=str(self.user),
            icon_url=str(self.user.avatar_url),
        )

        lc = self.get_channel(int(getenv("LOGS")))

        await lc.send(embed=embed)
