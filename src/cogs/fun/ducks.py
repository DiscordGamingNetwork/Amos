from discord.ext import commands

from os import getenv

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel


class Ducks(commands.Cog):
    """Turn yourself into a duck."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="duckify")
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.member)
    @in_channel(int(getenv("CHANNEL")))
    async def duckify(self, ctx: Context, unique: bool = False):
        """Get the duck version of yourself."""

        salt = ctx.message.id if unique else ""

        await ctx.reply(f"https://ducks.vcokltf.re/duck/{ctx.author.id}{salt}")


def setup(bot: Bot):
    bot.add_cog(Ducks(bot))
