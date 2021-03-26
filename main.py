from os import getenv
from dotenv import load_dotenv

from src.internal.bot import Bot


load_dotenv()

bot = Bot()

bot.load_extensions(
    "jishaku",
    "src.cogs.internal.error_handler",
    "src.cogs.internal.ping",
    "src.cogs.internal.update",
    "src.cogs.utility.bookmark",
    "src.cogs.core.topics",
    "src.cogs.fun.ducks",
)

bot.run(getenv("TOKEN"))
