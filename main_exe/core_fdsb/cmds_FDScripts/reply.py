# cmds_FDScripts/reply.py
import discord
from ..FDCore import ExecutionContext, Command, _ReplyWrapper

async def execute(cmd: Command, args: list[str], ctx: ExecutionContext, ch: discord.abc.Messageable) -> None:
    ctx.is_global_reply = True
    ctx._channel_override = _ReplyWrapper(ctx.message)
    ctx.log_event("reply → reply mode enabled")