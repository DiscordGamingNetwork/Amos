from discord.ext.commands import check

from .context import Context


def in_channel(*channels):
    async def predicate(ctx: Context):
        return ctx.channel.id in channels or ctx.author.id in ctx.bot.owner_ids

    return check(predicate)
