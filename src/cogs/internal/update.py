from discord import Embed
from discord.ext import commands

from os import system
from pathlib import Path

from src.internal.bot import Bot
from src.internal.context import Context



class Update(commands.Cog):
    """Run bot updates as a command."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(name="run")
    @commands.is_owner()
    async def run(self, ctx: Context):
        pass

    @run.command(name="update")
    async def update(self, ctx: Context):
        """Update the bot."""

        await ctx.reply(embed=Embed(
            title="Bot Restarting",
            colour=0x87CEEB,
        ))

        system("./update.sh")

    @run.command(name="pull")
    async def pull(self, ctx: Context):
        """Update the bot."""

        await ctx.reply(embed=Embed(
            title="Pulling from git...",
            colour=0x87CEEB,
        ))

        system("git pull origin master")

        await ctx.message.add_reaction("👌")

    @run.command(name="migrate")
    async def migrate(self, ctx: Context, filename: str):
        """Run a database migration."""

        p = Path(f"./src/data/{filename}.sql")

        with p.open() as f:
            await self.bot.db.execute(f.read())

        await ctx.reply(f"Successfully ran migration: `{filename}`")


def setup(bot: Bot):
    bot.add_cog(Update(bot))
