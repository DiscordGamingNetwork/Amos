from discord import Embed, TextChannel
from discord.ext import commands

from os import getenv
from re import compile

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel
from src.utils.msgfetch import fetch

LINK = compile(r"\bhttps://(canary\.|ptb\.)?discord\.com/channels/\d+/\d+/\d+\b")
IDID = compile(r"\b\d{17,20}-\d{17,20}\b")
ID = compile(r"\d+")



class Bookmark(commands.Cog):
    """Bookmark messages."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="bookmark", aliases=["bm"])
    @in_channel(int(getenv("CHANNEL")))
    async def run(self, ctx: Context, message: str):
        """
        Bookmark a message.

        Example usage: `.bm 825071171602874368-825093614853554196`
        """

        message = await fetch(message, ctx)

        if not message.content:
            return await ctx.reply("Message has no content, and can't be bookmarked.")

        embed = Embed(
            title="Bookmarked Message",
            colour=0x87CEEB,
            timestamp=message.created_at,
            description=message.content,
        )

        embed.set_footer(
            text=f"{self.bot.user} • Message sent:",
            icon_url=str(self.bot.user.avatar_url),
        )

        embed.set_author(
            name=str(message.author),
            icon_url=str(message.author.avatar_url),
        )

        embed.add_field(
            name="---",
            value=f"[Jump to original message]({message.jump_url})",
        )

        try:
            await ctx.author.send(embed=embed)
        except:
            return await ctx.reply("You need to enabled your DMs to bookmark messages.")

        await ctx.message.add_reaction("👌")


def setup(bot: Bot):
    bot.add_cog(Bookmark(bot))
