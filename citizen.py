from mongo import *


class Citizen:

    def __init__(self, name, lon, lat):
        self.name = name
        self.coordinates = {'lon': lon, 'lat': lat}

    async def save_myself(self):
        res_id = await MongoClient().do_insert(self.serialize())
        return res_id

    @property
    def user_name(self):
        return self.name

    @property
    def user_coordinates(self):
        return self.coordinates

    @property
    def user_lon(self):
        return self.coordinates['lon']

    @property
    def user_lat(self):
        return self.coordinates['lat']

    def serialize(self):
        return self.__dict__


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(Citizen('somename', 10, 10).save_myself())
