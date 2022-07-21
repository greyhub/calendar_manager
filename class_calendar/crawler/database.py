from pymongo import MongoClient
from config import MongoDBConfig, get_logger

logger = get_logger('MongoDB')


class Database:
    def __init__(self, url=None, timeout=10000):
        if url is None:
            url = f"mongodb://{MongoDBConfig.HOST}:{MongoDBConfig.PORT}"
        connection = MongoClient(url, serverSelectionTimeoutMS=timeout)
        self.db = connection[MongoDBConfig.DATABASE]
        self.class_schedule_col = self.db[MongoDBConfig.CLASS_SCHEDULE_COL]
        self.test_conn = connection.server_info()
        logger.info('Connected MongoDB!')

    def insert_class_schedule(self, schedule):
        self.class_schedule_col.insert_one(schedule)

    def get_class_schedule(self, student_id):
        key = {'_id': student_id}
        class_schedule = self.class_schedule_col.find_one(key)
        return class_schedule


# if __name__ == '__main__':
#     mongodb = Database(url='mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
#     # mongodb.write_class_schedule({"111": {'ifddd': 111}})
#     print(mongodb.get_class_schedule(20173261))
