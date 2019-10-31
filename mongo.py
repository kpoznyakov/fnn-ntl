from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('localhost', 27017)
db = client['test-database']
collection = db['citizen_mongo']


class MongoClient:

    async def do_insert(self, doc):
        result = await collection.insert_one(doc)
        return result.inserted_id

    async def do_count(self):
        res = await collection.estimated_document_count()
        # print(res)
        return res

    async def find(self, r={}, limit=0):
        cursor = collection.find(r).limit(limit)
        docs = await cursor.to_list(length=100)
        res = []
        while docs:
            for doc in docs:
                # print(doc)
                res.append(doc)
            docs = await cursor.to_list(length=100)
        return res


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(MongoClient().do_count())
    loop.run_until_complete(MongoClient().do_insert({'name': 'barrrr', 'coordinates': {'lon': 55, 'lat': 55}}))
