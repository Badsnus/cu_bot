import asyncio
from datetime import datetime, timedelta

from src.repo import DB
from src.services.get_db import get_db


def get_seconds_need_wait():
    now = datetime.now()
    day = now

    if now.hour >= 2:
        day += timedelta(days=1)

    next_event = datetime(
        year=day.year,
        month=day.month,
        day=day.day,
        hour=2,
    )

    seconds_until_next_day = (next_event - now).total_seconds()

    return seconds_until_next_day


@get_db
async def clear_old_logs(db: DB):
    need_wait = get_seconds_need_wait()
    await asyncio.sleep(int(need_wait))

    while True:
        await db.log.clear_old_logs()
        await asyncio.sleep(60 * 60 * 24)
