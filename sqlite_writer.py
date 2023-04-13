import aiosqlite
import sqlite3
import asyncio


async def a():
    async with aiosqlite.connect('hits_counter.sqlite') as db:
        await db.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')
        await db.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
        await db.execute("INSERT INTO stocks VALUES ('20020-01-05','BUY','RAT',14200,35.14)")
        await db.commit()


asyncio.run(a())
