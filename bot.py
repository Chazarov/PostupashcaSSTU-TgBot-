import logging
import emoji
import time

from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, text
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import config_bot as confB
from config import FACULTS
from Mes_shablon import MESSAGES

class Take_data(Helper):
    mode = HelperMode.snake_case

    GET_DATA = ListItem()
    DATA_ACCEPTED = ListItem()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=confB.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(state = None, commands = 'start')
async def command_start(message: types.Message):
    await message.answer(MESSAGES['inf'])

@dp.message_handler(state = None, commands = 'help')
async def command_halp(message: types.Message):
    await message.answer(MESSAGES['inf'])

@dp.message_handler(state = None, commands = 'my_results')
async def command_start(message:types.Message):
    state = dp.current_state(user = message.from_user.id)

    print(Take_data.all()[1])#check

    await state.set_state(Take_data.all()[1])
    await message.answer(MESSAGES['take_name'])

@dp.message_handler(state = Take_data.GET_DATA)
async def command_start(message:types.Message):
    name = message.text.split()
    state = dp.current_state(user = message.from_user.id)
    answer = ''
    for facult in FACULTS.keys():
        with open('facults' + '/' + facult + '.txt') as file:
            for line in file:
                if all(initials in line for initials in name):
                    answer += 'В списке на факультете ' + facult + ' вы на месте ' + line[:8][2:] + '\n'
    if answer == '':
        await state.set_state()
        return await message.answer(MESSAGES['not_found_name'])
    else:
        await state.set_state()
        return await message.answer(answer)


@dp.message_handler(state = None)
async def command_halp(message: types.Message):
    if message.text not in FACULTS.keys():
        await message.answer(MESSAGES['not_expect'])
    else:
        with open('facults' + '/' + message.text + '.txt') as file:
            answer = ''
            count = 0
            for i in file:
                answer += i
                count += 1
                if count == 14:
                    await message.answer(answer)
                    time.sleep(1.5)
                    count = 0
                    answer = ''
            await message.answer(answer)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)