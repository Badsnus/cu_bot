import asyncio
from datetime import datetime, timedelta

from src.repo import DB
from src.services.get_db import get_db


def get_seconds_need_wait():
    now = datetime.now()

    next_day = now + timedelta(days=1)

    next_day_start = datetime(next_day.year, next_day.month, next_day.day, hour=2)

    seconds_until_next_day = (next_day_start - now).total_seconds()

    return seconds_until_next_day


@get_db
async def clear_old_logs(db: DB):
    need_wait = get_seconds_need_wait()
    await asyncio.sleep(int(need_wait))

    while True:
        await db.log.clear_old_logs()
        await asyncio.sleep(60 * 60 * 24)
