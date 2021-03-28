from discord import Embed
from discord.ext import commands

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel

EMOJI = "🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯".split(" ")


class Polls(commands.Cog):
    """Create poll embeds - staff only."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="poll")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def poll(self, ctx: Context, name: str, *options):
        """Create a poll."""

        desc = ""
        for i, option in enumerate(options):
            desc += f"{EMOJI[i]} {option}\n"

        embed = Embed(
            title=name,
            colour=0x87CEEB,
            description=desc,
        )

        msg = await ctx.reply(embed=embed)

        for i in range(len(options)):
            await msg.add_reaction(EMOJI[i])


def setup(bot: Bot):
    bot.add_cog(Polls(bot))
