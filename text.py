from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import link
import json
from random import choice
from os.path import isfile
token = 'tg_bot_token'
admins_list = [123, 456]
channels = ['channels for subscribe']

bot = Bot(token=token)
dp = Dispatcher(bot)
if not isfile('participants.malw'):
    open('participants.malw', 'w').close()

with open('participants.malw', 'r') as file:
    participants = json.loads(file.read())

@dp.message_handler(commands='start')
async def start(message: types.Message):
    global participants, channels
    if str(message['from']['id']) in participants:
        await message.reply('You are already in the draw')
        return
    for channel in channels:
        try:
            user_info = await bot.get_chat_member(channel, message['from']['id'])
            if user_info['status'] not in ['member', 'creator', 'administrator']:
                raise
        except Exception as e:
            channel_info = await bot.get_chat(channel)
            await message.reply('You are not subscribed to '+link(channel_info['title'], 'https://t.me/'+channel_info['username']), parse_mode='markdown')
            return
    participants.append(str(message['from']['id']))
    with open('participants.malw', 'w') as file:
        file.write(json.dumps(participants))
    await message.reply('You entered the draw')

@dp.message_handler(commands='check')
async def check(message: types.Message):
    global participants, channels
    if message['from']['id'] in admins_list:
        for participant in participants:
            for channel in channels:
                try:
                    user_info = await bot.get_chat_member(channel, message['from']['id'])
                    if user_info['status'] not in ['member', 'creator', 'administrator']:
                        raise
                except Exception as e:
                    channel_info = await bot.get_chat(channel)
                    await bot.send_message(participant, 'you left the channel '+link(channel_info['title'], 'https://t.me/'+channel_info['username'])+'ERROR', parse_mode='markdown')
                    participants.remove(participant)
                    break
        with open('participants.malw', 'w') as file:
            file.write(json.dumps(participants))
        await message.reply('Verification completed')

@dp.message_handler(commands='end')
async def end(message: types.Message):
    global participants
    if message['from']['id'] in admins_list:
        if participants == []:
            await message.reply('Nobody participates in the draw')
            return
        winner = choice(participants)
        winner_name = await bot.get_chat(winner)
        for participant in participants:
            try:
                await bot.send_message(int(participant), 'A fair system of chance determined the winner of this draw. Its getting '+link(winner_name['first_name'], 'tg://user?id='+winner), parse_mode='markdown')
            except:
                pass
        await message.reply('A fair system of chance determined the winner of this draw. Its getting '+link(winner_name['first_name'], 'tg://user?id='+winner), parse_mode='markdown')
        participants = []
        with open('participants.malw', 'w') as file:
            file.write(json.dumps(participants))

if '__main__' == __name__:
    print(__name__)
    executor.start_polling(dp, skip_updates=True)

#full code in telegram channel

#full code in telegram channel

#full code in telegram channel