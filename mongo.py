from mongo_thingy import connect, Thingy

connect("mongodb://localhost/test-database")
print('Connected to Mongo!')


class Citizen2Mongo(Thingy):
    pass
