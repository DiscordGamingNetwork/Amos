from re import compile

from src.internal.context import Context


LINK = compile(r"\bhttps://(canary\.|ptb\.)?discord\.com/channels/\d+/\d+/\d+\b")
IDID = compile(r"\b\d{17,20}-\d{17,20}\b")
ID = compile(r"\d+")

async def fetch(message: str, ctx: Context):
    lmatch = LINK.match(message)
    imatch = IDID.match(message)

    if not (lmatch or imatch):
        return await ctx.send_help(ctx.command.name)

    ids = ID.findall(message)
    mod = 0 if imatch else 1

    channel = ctx.guild.get_channel(int(ids[0 + mod]))
    if not channel:
        return await ctx.reply("Invalid message.")

    pf = channel.permissions_for(ctx.author)
    if not pf.view_channel:
        return await ctx.reply("You're not allowed to access that message.")

    try:
        message = await channel.fetch_message(int(ids[1 + mod]))
    except:
        return await ctx.reply("Invalid message")

    return message
