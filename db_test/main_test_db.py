from orm import SyncOrmWorker, AsyncOrm

SyncOrmWorker.create_tables()
SyncOrmWorker.insert_workers()

SyncOrmWorker.update_worker(1, "w1")

