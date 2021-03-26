from discord import Embed
from discord.ext import commands

from os import system

from src.internal.bot import Bot
from src.internal.context import Context



class Update(commands.Cog):
    """Run bot updates as a command."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="update")
    @commands.is_owner()
    async def ping(self, ctx: Context):
        """Update the bot."""

        await ctx.reply(embed=Embed(
            title="Bot Restarting",
            colour=0x87CEEB,
        ))

        system("./update.sh")


def setup(bot: Bot):
    bot.add_cog(Update(bot))
