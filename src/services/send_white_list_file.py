import os
import uuid

from aiogram.types import CallbackQuery, FSInputFile

from src.repo import DB
from src.services.get_db import get_db


@get_db
async def send_white_list_file(chat_id: int, call: CallbackQuery, db: DB) -> None:
    filename = str(uuid.uuid4()) + '.txt'

    data = await db.white_list.get_by_chat(chat_id)

    with open(filename, 'w') as file:
        file.write('\n'.join('@' + w.username for w in data))

    try:

        await call.message.answer_document(document=FSInputFile(filename, 'white_list.txt'))

        try:
            os.remove(filename)
        except:
            pass
    except:
        await call.message.answer('White list пуст')
