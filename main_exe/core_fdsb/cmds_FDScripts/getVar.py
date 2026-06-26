# cmds_FDScripts/getVar.py
import discord
from main_exe.core_fdsb.FDCore import (
    ExecutionContext, Command,
    FDLogicError, FDRuntimeError,
    _send_error, _load_data, _load_ids_data, _truncate,
)

def _fmt(err) -> str:
    return f"{err._icon} **{err._category}** — {err.msg}"

def resolve_inline(args: list[str], ctx: ExecutionContext) -> str:
    if len(args) == 2:
        name    = args[0].strip()
        user_id = args[1].strip()
        if not name:
            return _fmt(FDLogicError("`$getVar` — variable name cannot be empty."))
        if not user_id:
            return _fmt(FDLogicError("`$getVar` — user ID cannot be empty."))
        data = _load_ids_data()
        val  = data.get(name, {}).get(user_id, '')
        ctx.log_event(f"getVar [{name}] for user {user_id} → {_truncate(val)!r}")
        return str(val)

    elif len(args) == 1:
        name = args[0].strip()
        if not name:
            return _fmt(FDLogicError("`$getVar` — variable name cannot be empty."))
        data = _load_data()
        if name not in data:
            return _fmt(FDRuntimeError(
                f"`$getVar[{name}]` — variable `{name}` does not exist.\n"
                f"Tip: Create it first from the Variables tab in BCFD."
            ))
        value = str(data[name])
        ctx.log_event(f"getVar [{name}] → {_truncate(value)!r}")

        from main_exe.core_fdsb.FDCore import _VARS_DIR
        print(f"[getVar DEBUG] looking for: '{name}' in: '{_VARS_DIR}'")
        data = _load_data()
        print(f"[getVar DEBUG] found keys: {list(data.keys())}")

        return value

    else:
        return _fmt(FDLogicError(
            "`$getVar` requires 1 or 2 arguments: `$getVar[name]` or `$getVar[name; user_id]`"
        ))

async def execute(cmd: Command, args: list[str], ctx: ExecutionContext, ch: discord.abc.Messageable) -> None:
    result = resolve_inline([ctx.resolve(a) for a in args], ctx)
    if result:
        await ch.send(result)