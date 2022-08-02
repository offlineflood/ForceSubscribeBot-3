from platform import python_version as pyver
from telegram import __version__ as telever
from pyrogram import __version__ as pyrover
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters

@Client.on_message(filters.incoming & filters.command(['repo', 'repo@FSubsRobot']))
async def repo(_, message):
    await message.reply_text(
        f"""✨ **Hey I'm Force Subscribe** 
**Owner repo : [Fariz](https://t.me/Farizsj)**
**Python Version :** `{pyver()}`
**Library Version :** `{telever}`
**Pyrogram Version :** `{pyrover}`
**Create your own with click button bellow.**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Repo", url="https://github.com/farizjs/ForceSubscribe"), 
                    InlineKeyboardButton(
                        "Support", url="https://t.me/FlicksSupport")
                ]
            ]
        ),
        disable_web_page_preview=True
    )
