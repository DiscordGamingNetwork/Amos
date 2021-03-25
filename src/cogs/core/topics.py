from discord import Embed
from discord.ext import commands

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel


class Topics(commands.Cog):
    """Get topics for discussion."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="topic")
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.channel)
    @in_channel(264417177094848512, 737760236013748295, 779479420481175554)
    async def get_topic(self, ctx: Context):
        """Get a topic to talk about."""

        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        topic = await self.bot.db.get_random_topic()

        embed = Embed(
            description=topic["topic"],
            colour=0x87CEEB,
            timestamp=topic["created_at"],
        )

        user = ctx.guild.get_member(topic["author_id"])

        embed.set_footer(
            text=f"From: {user if user else 'unknown'} • ID: {topic['id']} • Created:"
        )

        await ctx.reply(embed=embed)

    @commands.command(name="newtopic")
    @commands.cooldown(rate=1, per=600, type=commands.BucketType.member)
    @in_channel(264417177094848512, 737760236013748295)
    async def new_topic(self, ctx: Context, *, topic: str):
        """Create a new topic."""

        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        if len(topic) > 200:
            return await ctx.reply("Topics must be 200 characters or less.")

        topic = await self.bot.db.create_topic(ctx.author.id, topic)

        await ctx.reply(f"Topic created! ID: {topic['id']}")

    @commands.command(name="deltopic")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def del_topic(self, ctx: Context, id: int):
        """Delete a topic."""

        await self.bot.db.delete_topic(id)

        await ctx.message.add_reaction("👌")

    @commands.command(name="topicinfo")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def del_topic(self, ctx: Context, id: int):
        """Get information about a topic."""

        topic = await self.bot.db.get_topic_by_id(id)

        if not topic:
            return await ctx.reply("Not a valid topic.")

        await ctx.reply(f"ID: {topic['id']}\nCreated by: {ctx.guild.get_member(topic['author_id'])} ({topic['author_id']})\nData:```\n{topic['topic']}```")


def setup(bot: Bot):
    bot.add_cog(Topics(bot))
