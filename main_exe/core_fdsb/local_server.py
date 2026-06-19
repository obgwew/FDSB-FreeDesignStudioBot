# Copyright (C) 2026 obgwew
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
# main_exe/core_fdsb/local_server.py 

import discord
from discord.ext import commands
import json
import os
import asyncio
import threading
import time
from main_exe.core_fdsb.FDScript import run_script
from main_exe.core_fdsb.FDCore   import set_vars_dir, set_bot_start_time

# ══════════════════════════════════════════════════════════════
#  PrefixManager 
# ══════════════════════════════════════════════════════════════

class PrefixManager:
    def __init__(self):
        self._bot_commands_dir = ''
        self._bot_events_dir = ''  

    def set_bot_dir(self, bot_dir: str):
        abs_dir = os.path.abspath(bot_dir)
        if os.path.basename(abs_dir).lower() == 'bot_files':
            bot_root = os.path.dirname(abs_dir)
        else:
            bot_root = abs_dir
        self._bot_commands_dir = os.path.join(bot_root, 'bot_commands')
        self._bot_events_dir = os.path.join(bot_root, 'bot_events') 

    def get_event_scripts(self, event_name: str) -> list[str]:
        results: list[str] = []
        if not os.path.isdir(self._bot_events_dir):
            return results

        for fname in sorted(os.listdir(self._bot_events_dir)):
            fpath = os.path.join(self._bot_events_dir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if not content.strip():
                    continue

                first_line = content.split('\n')[0].strip().replace(" ", "").upper()
                if first_line.startswith("#PREFIX:"):
                    prefix_part = first_line.replace("#PREFIX:", "").split('[')[0]
                    if prefix_part == event_name.upper():
                        results.append(content)
            except Exception:
                pass
        return results

    def get_script_by_message(self, message_content: str) -> str | None:
        if not os.path.isdir(self._bot_commands_dir):
            return None

        for fname in os.listdir(self._bot_commands_dir):
            fpath = os.path.join(self._bot_commands_dir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    continue
                
                first_line = content.split('\n')[0].strip()
                if first_line.upper().startswith("#PREFIX:"):
                    prefix = first_line.split(":", 1)[1].strip()
                    after = message_content.strip()[len(prefix):]
                    if message_content.strip().startswith(prefix) and (not after or after[0].isspace()):
                        return content
            except Exception:
                pass
        return None


# ─────────────────────────────────────────────────────────────
#  setting up the bot 
# ─────────────────────────────────────────────────────────────

_client          = None
_thread          = None
_loop            = None
_stopping        = False
_vars_dir_path   = ''
prefix_manager   = PrefixManager()


def get_vars_dir() -> str:
    return _vars_dir_path


def _get_token(bot_dir: str) -> str:
    possible_paths = [
        os.path.join(bot_dir, 'config.json'),
        os.path.join(bot_dir, 'bot_files', 'config.json'),
        os.path.join(os.path.dirname(bot_dir), 'config.json'),
        os.path.join(os.path.dirname(bot_dir), 'bot_files', 'config.json'),
    ]

    print(f"[DEBUG] bot_dir : {bot_dir}")

    for path in possible_paths:
        print(f"[DEBUG] Searching in: {path}")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                
                token = data.get('token') or data.get('TOKEN') or data.get('bot_token')
                if token:
                    print(f"[DEBUG] ✅ Token found in: {path}")
                    return str(token)
                else:
                    print(f"[DEBUG] File exists but does not contain 'token'")
            except Exception as e:
                print(f"[ERROR] Failed to read {path}: {e}")

    print("[Bot] ❌ config.json not found in any expected path")
    return ''


# ══════════════════════════════════════════════════════════════
# event_FDScripts
# ══════════════════════════════════════════════════════════════

def _make_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"[Bot] Logged in successfully as: {bot.user}")
        set_bot_start_time(time.time())

    # ── $onJoined ──
    @bot.event
    async def on_member_join(member):
        scripts = prefix_manager.get_event_scripts("$onJoined")
        if not scripts:
            return
        from main_exe.core_fdsb.event_FDScripts.onJoined import handle_event
        for script_text in scripts:
            try:
                await handle_event(member, bot, script_text)
            except Exception as e:
                print(f"[Bot] Error executing $onJoined event: {e}")

    # ── $onLeave ──
    @bot.event
    async def on_member_remove(member):
        scripts = prefix_manager.get_event_scripts("$onLeave")
        if not scripts:
            return
        from main_exe.core_fdsb.event_FDScripts.onLeave import handle_event
        for script_text in scripts:
            try:
                await handle_event(member, bot, script_text)
            except Exception as e:
                print(f"[Bot] Error executing $onLeave event: {e}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        # ── $alwaysReply ──
        always_scripts = prefix_manager.get_event_scripts("$alwaysReply")
        if always_scripts:
            try:
                from main_exe.core_fdsb.event_FDScripts.alwaysReply import handle_event as handle_always_reply
                for script_text in always_scripts:
                    await handle_always_reply(message, bot, script_text)
            except Exception as e:
                print(f"[Bot] Error executing $alwaysReply event: {e}")

        script_text = prefix_manager.get_script_by_message(message.content)
        if script_text is not None:
            try:
                await run_script(message, bot, script_text)
            except Exception as e:
                print(f"[Bot] Error executing script: {e}")
            return

        await bot.process_commands(message)

    return bot


# ══════════════════════════════════════════════════════════════
#  Threading
# ══════════════════════════════════════════════════════════════

def _runner(token: str):
    global _loop, _client, _stopping
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    
    try:
        _loop.run_until_complete(_client.start(token))
    except Exception as e:
        print(f"[Bot] Stopped after error: {e}")
    finally:
        _stopping = False
        _client = None


def start_bot(bot_dir: str) -> bool:
    global _client, _thread, _stopping, _vars_dir_path

    if _stopping:
        print("[Bot] Still stopping, please wait")
        return False

    if _client and not _client.is_closed():
        print("[Bot] Bot is already online")
        return False

    token = _get_token(bot_dir)
    if not token:
        print("[Bot] config.json not found")
        return False

    prefix_manager.set_bot_dir(bot_dir)

    abs_bot_dir = os.path.abspath(bot_dir)
    if os.path.basename(abs_bot_dir).lower() == 'bot_files':
        bot_root = os.path.dirname(abs_bot_dir)
    else:
        bot_root = abs_bot_dir

    _vars_dir_path = os.path.join(bot_root, 'bot_vars')
    os.makedirs(_vars_dir_path, exist_ok=True)
    set_vars_dir(_vars_dir_path)
    print(f"[Bot] _vars_dir_path → {_vars_dir_path}")

    _client = _make_bot()
    _thread = threading.Thread(target=_runner, args=(token,), daemon=True)
    _thread.start()
    print("[Bot] Bot is now online")
    return True


def stop_bot() -> None:
    global _stopping
    if _stopping:
        return
    if _client is None or _client.is_closed():
        return
    _stopping = True
    if _loop and _loop.is_running():
        asyncio.run_coroutine_threadsafe(_client.close(), _loop)