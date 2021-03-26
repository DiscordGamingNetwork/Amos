from discord import Embed, File, Reaction, Member, Message
from discord.ext import commands

from io import StringIO
from collections import namedtuple
from time import time

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel


class TopicMessage:
    def __init__(self, message: Message):
        self.msg = message
        self.time = time()
        self.users = set()


class Topics(commands.Cog):
    """Get topics for discussion."""

    def __init__(self, bot: Bot):
        self.bot = bot

        self.messages = None

    async def gen_topic(self):
        topic = await self.bot.db.get_random_topic()

        embed = Embed(
            description=topic["topic"],
            colour=0x87CEEB,
            timestamp=topic["created_at"],
        )

        user = self.bot.get_user(topic["author_id"])

        embed.set_footer(
            text=f"From: {user if user else 'unknown'} • ID: {topic['id']} • Created:"
        )

        return embed

    @commands.command(name="topic")
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.channel)
    @in_channel(264417177094848512, 737760236013748295, 779479420481175554)
    async def get_topic(self, ctx: Context):
        """Get a topic to talk about."""

        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        embed = await self.gen_topic()

        msg = await ctx.reply(embed=embed)

        await msg.add_reaction("🔁")

        self.message = TopicMessage(msg)

    @commands.command(name="newtopic")
    @commands.cooldown(rate=1, per=600, type=commands.BucketType.member)
    @commands.check_any(commands.is_owner(), commands.has_any_role(339445127917338635, 337442104026595329))
    @in_channel(264417177094848512, 737760236013748295)
    async def new_topic(self, ctx: Context, *, topic: str):
        """Create a new topic."""

        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        if len(topic) > 200:
            return await ctx.reply("Topics must be 200 characters or less.")

        topic = await self.bot.db.create_topic(ctx.author.id, topic)

        await ctx.reply(f"Topic created! ID: {topic['id']}")

    @commands.command(name="importtopics")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def import_topics(self, ctx: Context):
        """Import topics from a text file."""

        if not ctx.message.attachments:
            return await ctx.reply("You must attach a file for this.")

        async with ctx.typing():
            file = await self.bot.sess.get(ctx.message.attachments[0].url)
            file = await file.text()

            ids = []

            for line in file.split("\n"):
                if line:
                    topic = await self.bot.db.create_topic(ctx.author.id, line)
                    ids.append(topic['id'])

            await ctx.reply(f"Successfully inserted {len(ids)} topics")

    @commands.command(name="deltopic")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def del_topic(self, ctx: Context, id: int):
        """Delete a topic."""

        await self.bot.db.delete_topic(id)

        await ctx.message.add_reaction("👌")

    @commands.command(name="topicinfo")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def topic_info(self, ctx: Context, id: int):
        """Get information about a topic."""

        topic = await self.bot.db.get_topic_by_id(id)

        if not topic:
            return await ctx.reply("Not a valid topic.")

        await ctx.reply(f"ID: {topic['id']}\nCreated by: {ctx.guild.get_member(topic['author_id'])} ({topic['author_id']})\nData:```\n{topic['topic']}```")

    @commands.command(name="lstopics")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def list_topics(self, ctx: Context):
        """List all topics."""

        topics = await self.bot.db.get_topics()

        data = "\n".join([f"{str(topic['id']).zfill(4)}: {topic['topic']}" for topic in topics])

        await ctx.reply(f"There are a total of {len(topics)} topics:", file=File(StringIO(data), filename="topics.txt"))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, member: Member):
        """Allows for refreshing the topic."""

        if not isinstance(member, Member):
            return

        if member == self.bot.user:
            return

        if not self.message:
            return

        if self.message.msg.id != reaction.message.id:
            return

        if self.message.time + 30 < time():
            return

        self.message.users.add(member.id)

        if len(self.message.users) >= 4:
            await self.message.msg.edit(embed=await self.gen_topic())
            self.message = None


def setup(bot: Bot):
    bot.add_cog(Topics(bot))
