from discord import Embed
from discord.ext import commands

from os import getenv
from pyowo import owo

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel
from src.utils.msgfetch import fetch


class Misc(commands.Cog):
    """Miscellaneous fun commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="owoify", aliases=["owo"])
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.member)
    @in_channel(int(getenv("CHANNEL")))
    async def owoify(self, ctx: Context, message: str):
        """
        Get the owo'd version of a message.

        Example usage: `.owo 825071171602874368-825093614853554196`
        """

        message = await fetch(message, ctx)

        if not message:
            return await ctx.reply("I couldn't find that message.")

        if not message.content:
            return await ctx.reply("Message has no content, and can't be bookmarked.")

        embed = Embed(
            title="OwO'd Message",
            colour=0x87CEEB,
            timestamp=message.created_at,
            description=owo(message.content),
        )

        embed.set_footer(
            text=f"{self.bot.user} • Message sent:",
            icon_url=str(self.bot.user.avatar_url),
        )

        embed.set_author(
            name=str(message.author),
            icon_url=str(message.author.avatar_url),
        )

        await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Misc(bot))
