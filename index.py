from pyrogram import Client,filters,idle
import asyncio

loop = asyncio.get_event_loop()

app = Client(
    "namendndb",
    api_id=9176863,
    api_hash="afff208ad0de11acfc946ca6dcd74aec",
    bot_token="7960951037:AAHd0KUC59z0_B4i6W5AwIfjlb0VqLSHX-k",
)

@app.on_message(filters.command("start") & filters.private)
async def start(client,message):
    return await message.reply_animation("https://porngifmag.com/content/2017/02/porn-gif-magazine-italiansd0itbetter-2.gif",caption="**FUCKING KCAK HARD CORE**")


async def exe():
    await app.start()
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop.run_until_complete(exe())
