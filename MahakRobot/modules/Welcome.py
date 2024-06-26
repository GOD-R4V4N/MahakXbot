import os
import random
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger

from MahakRobot import pbot as app

from MahakRobot.database.wel_db import *

COMMAND_HANDLER = ". /".split() # COMMAND HANDLER

LOGGER = getLogger(__name__)

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chat, id, uname):
    background = Image.open("MahakRobot/resources/bg.jpg")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize(
        (605, 605)
    ) 
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('MahakRobot/resources/SwanseaBold-D0ox.ttf', size=75)
    welcome_font = ImageFont.truetype('MahakRobot/resources/SwanseaBold-D0ox.ttf', size=90)
    draw.text((150, 450), f'NAME : {unidecode(user)}', fill="black", font=font)
    draw.text((150, 550), f'ID : {id}', fill="black", font=font)
    draw.text((150, 650), f"USERNAME : {uname}", fill="black",font=font)
    pfp_position = (1077, 183)  
    background.paste(pfp, pfp_position, pfp)  
    background.save(
        f"downloads/welcome#{id}.png"
    )
    return f"downloads/welcome#{id}.png"

#######

@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    #A = await wlcm.find_one({"chat_id" : chat_id})
    #if not A:
      # return
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"left"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "HuTao/resources/profilepic.jpg"
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption= f"""
**ㅤㅤㅤ◦•●◉✿ ᴡᴇʟᴄᴏᴍᴇ ʙᴀʙʏ ✿◉●•◦
▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰

● ɢʀᴏᴜᴘ ➥ {member.chat.title}
● ɴᴀᴍᴇ ➥ {user.mention}
● ᴜsᴇʀ ɪᴅ ➥ {user.id}
● ᴜsᴇʀɴᴀᴍᴇ ➥ @{user.username}

❖ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ ๛ᴍ ᴀ ʜ ᴀ ᴋ ࿐ **
▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▰
""",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton (f"ᴠɪᴇᴡ ᴜsᴇʀ", url=f"https://t.me/{user.username}")]])

            )
    except Exception as e:
        LOGGER.error(e)
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        return 


#####
