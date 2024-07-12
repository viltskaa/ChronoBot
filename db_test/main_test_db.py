from orm import SyncOrmWorker, AsyncOrm
import asyncio
from datetime import datetime

# asyncio.run(AsyncOrm.create_tables())
asyncio.run(AsyncOrm.insert_time(1,
                                 'POLKA01',
                                 datetime.strptime('15:00', '%H:%M'),
                                 16634.4))

asyncio.run(AsyncOrm.insert_time(2,
                                 'POLKA02',
                                 datetime.strptime('12:00', '%H:%M'),
                                 455.12))


# SyncOrmWorker.create_tables()
# SyncOrmWorker.insert_workers()

# SyncOrmWorker.update_worker(1, "w1")

