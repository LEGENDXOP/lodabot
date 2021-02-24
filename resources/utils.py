import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
CMD_LIST = {}
session_name = str(Var.STRING_SESSION)
if session_name.endswith("="):
     bot = TelegramClient(StringSession(session_name), Var.APP_ID, Var.API_HASH)
else:
     bot = TelegramClient(
         "TG_BOT_TOKEN", api_id=Var.APP_ID, api_hash=Var.API_HASH
     ).start(bot_token=Var.STRING_SESSION)

def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        else:
            if len(Config.COMMAND_HAND_LER) == 2:
                catreg = "^" + Config.COMMAND_HAND_LER
                reg = Config.COMMAND_HAND_LER[1]
            elif len(Config.COMMAND_HAND_LER) == 1:
                catreg = "^\\" + Config.COMMAND_HAND_LER
                reg = Config.COMMAND_HAND_LER
            args["pattern"] = re.compile(catreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})

    args["outgoing"] = True
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    args["blacklist_chats"] = True
    black_list_chats = list(Config.UB_BLACK_LIST_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    # add blacklist chats, UB should not respond in these chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        args["allow_edited_updates"]
        del args["allow_edited_updates"]

    # check if the plugin should listen for outgoing 'messages'

    return events.NewMessage(**args)
