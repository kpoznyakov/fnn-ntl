from mongo import *


class Citizen:

    def __init__(self, name, lon, lat):
        self.name = name
        self.coordinates = {'lon': lon, 'lat': lat}
        self.mongo_obj = Citizen2Mongo(self.serialize()).save()
        self.id = self.mongo_obj.id

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
