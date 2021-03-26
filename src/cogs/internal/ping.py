from discord import Embed
from discord.ext import commands

from time import time
from collections import namedtuple

from src.internal.bot import Bot
from src.internal.context import Context


TimedResult = namedtuple('TimedResult', ["time", "rv"])


class Topics(commands.Cog):
    """Get topics for discussion."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def timed_coro(coro):
        ts = time()
        rs = await coro
        return TimedResult(round((time() - ts) * 1000, 2), rs)

    @commands.command(name="ping")
    @commands.is_owner()
    async def ping(self, ctx: Context):
        """Beefy ass ping command."""

        msend = await self.timed_coro(ctx.send("Pinging..."))
        medit = await self.timed_coro(msend.rv.edit(content="Editing..."))
        msdel = await self.timed_coro(msend.rv.delete())

        embed = Embed(
            title="Ping",
            colour=0x87CEEB,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="WS Latency", value=f"{round(self.bot.latency * 1000, 2)}ms", inline=False)
        embed.add_field(name="API Send", value=f"{msend.time}ms", inline=True)
        embed.add_field(name="API Edit", value=f"{medit.time}ms", inline=True)
        embed.add_field(name="API Delete", value=f"{msdel.time}ms", inline=True)

        await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Topics(bot))
