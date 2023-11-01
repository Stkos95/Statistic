# from pymongo import MongoClient
# from config import load_config
#
# config = load_config()
# MONGO_USER = config.database.user
# MONGO_PASSWORD = config.database.password
# MONGO_CONTAINER_NAME = config.database.container
#
#
# URL = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@127.0.0.1:27017/admin?directConnection=true&appName=mongosh+1.10.6'
#
# client = MongoClient(URL)
#
#
#
# def db_processing(database='new_data'):
#     return client.new_data
# #
# #
#
# db = client.new_data
# # print(db.list_collection_names())
# #
# res = db.test.find()
# print(res)
# res = map(lambda x: str(x['_id']), res)
# for i in res:
#     print(i)
#
