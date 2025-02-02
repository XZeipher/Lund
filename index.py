from pyrogram import Client,filters,idle
import asyncio

loop = asyncio.get_event_loop()

app = Client(
    "namendndb",
    api_id=9176863,
    api_hash="afff208ad0de11acfc946ca6dcd74aec",
    session_string="BQElrxsAD6-pMTvtiXz5Sq6xkbzhwikfAqE0TRgDpgLD51CufFrOWH9mL7ceo1y0dkRhIRq44lGKsIveUlaGnhQSQJ-kgShrK62P_Xc_rZR0nouUYw1MT9RBnwrRj8AMtjaoeqG1yvzaBT_9AbGQbROZl5OkH6tq6CJIuxfBVsoS4tA0dpQTFfF13pNmirvKxC1F1jX-Yb0ixjlL-dkl11NvP6Tex0V53K0D03NXFLVYtgaR8d8bMqSPcZuQs2hgN2eRJ7JRnAWJ0DjErTO71dkTjYU-wq8JLmXUpcgtNav01fQWH6GBtUquEhCSKTDV6EbRcafm1AxsrsqUj5QF6DZL8aEbjQAAAAHjfkczAA",
)

@app.on_message(filters.command("alive", prefixes=["?"]) & filters.me)
async def start(client,message):
    return await message.reply_text("I am alive!")

import io
from re import sub
import sys
import traceback
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import RPCError
import subprocess
from datetime import datetime
from pyrogram import filters, enums ,Client

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@app.on_message(filters.command(["run","eval", "e"], prefixes=["?"]) & filters.me)
async def eval(client, message):
    if len(message.text.split()) < 2:
        return await message.reply_text("`Input Not Found!`")
    
    cmd = message.text.split(maxsplit=1)[1]     
    status_message = await message.reply_text("Processing ...")    
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    end = datetime.now()
    ping = (end-start).microseconds / 1000
    final_output = "<b>📎 Input</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>📒 Output</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n\n"
    final_output += f"<b>✨ Taken Time</b>: {ping}<b>ms</b>"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await status_message.edit_text(final_output)

async def exe():
    await app.start()
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop.run_until_complete(exe())
