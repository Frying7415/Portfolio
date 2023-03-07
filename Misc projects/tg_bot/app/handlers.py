# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 18:36:17 2022

@author: HP
"""

from telethon import events
from __init__ import bot
from mail_body import random_text

@bot.on(events.NewMessage(chats=CHAT_ID))
async def my_event_handler(event):
    if 'Привет' in event.raw_text:
        await event.respond(
            '''Привет!\
Чтобы получить цитату, напиши "Дай цитату".
Чтобы получить ещё одну, напиши "Дай ещё".'''
        )
    elif 'дай цитату' in event.raw_text.lower():
        await event.reply('Уже ищу подходящую...')
        await bot.send_message(CHAT_ID, random_text())
    elif 'дай ещё' in event.raw_text.lower():
        await event.reply('Вот, держи:')
        await bot.send_message(CHAT_ID, random_text())