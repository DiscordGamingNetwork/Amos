from discord.ext import commands

from os import getenv

from src.internal.bot import Bot
from src.internal.context import Context
from src.internal.checks import in_channel


class Trivia(commands.Cog):
    """Trivia questions."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(name="trivia", invoke_without_command=True)
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.member)
    @in_channel(int(getenv("CHANNEL")))
    async def trivia(self, ctx: Context, unique: bool = False):
        """Get a trivia question."""

        pass

    @trivia.command(name="add")
    @commands.check_any(commands.is_owner(), commands.has_role(337442104026595329))
    async def trivia_add(self, ctx: Context, *, question: str):
        """Add a new trivia question."""

        await ctx.reply("Enter valid answers, and .stop to finish.")

        answers = []

        while True:
            try:
                msg = await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timeout=15)
            except:
                return await ctx.reply("Selection timed out, exiting.")
            answer = msg.content

            if answer == ".stop":
                break
            else:
                answers.append(answer)

        answers = "`".join(answers)

        await self.bot.db.create_trivia_question(ctx.author.id, question, answers)


def setup(bot: Bot):
    bot.add_cog(Trivia(bot))
