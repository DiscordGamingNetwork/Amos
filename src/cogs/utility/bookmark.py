from discord import Embed, TextChannel
from discord.ext import commands

from os import getenv
from re import compile

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel

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

        lmatch = LINK.match(message)
        imatch = IDID.match(message)

        if not (lmatch or imatch):
            return await ctx.send_help("bm")

        ids = ID.findall(message)
        mod = 0 if imatch else 1

        channel = ctx.guild.get_channel(int(ids[0 + mod]))
        if not channel:
            return await ctx.reply("Invalid message.")

        pf = channel.permissions_for(ctx.author)
        if not pf.view_channel:
            return await ctx.reply("You're not allowed to access that message, so I can't create a bookmark for it.")

        try:
            message = await channel.fetch_message(int(ids[1 + mod]))
        except:
            return await ctx.reply("Invalid message")

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
