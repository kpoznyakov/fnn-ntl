from aiohttp import web

from citizen import *

routes = web.RouteTableDef()


@routes.post('/users')
async def create_citizen(request):
    d = await request.json()
    if not d.get('lon') or not d.get('lat'):
        return web.Response(text='lon or lat not found.', status=400)
    if not d.get('name'):
        return web.Response(text='name not found.', status=400)
    if not -180 <= d.get('lon') <= 180 or not -90 <= d.get('lat') <= 90:
        return web.Response(text='lon or lat out of range.', status=400)
    c = Citizen(**d)
    await c.save_myself()
    return web.json_response(text=str(c.serialize()), status=201)


@routes.get('/users')
async def get_citizens(request):
    limit = 10000
    response = {'total': await MongoClient().do_count(),
                'request_limit': limit,
                'users': await MongoClient().find(limit=limit)}
    return web.json_response(text=str(response))


async def do_find(r, limit):
    cursor = collection.find(r).limit(limit)
    for document in await cursor.to_list(length=3):
        print(document)


@routes.get('/lookup')
async def get_nearest(request):
    d = request.query
    lon = float(d.get('lon'))
    lat = float(d.get('lat'))
    radius = int(d.get('radius')) * 1000  # meters to kilometers
    limit = int(d.get('limit'))

    if not -180 <= lon <= 180 or not -90 <= lat <= 90:
        return web.Response(text='lon or lat out of range.', status=400)

    r = {'coordinates': {
        '$near': {
            '$geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]
            },
            '$maxDistance': radius
        }
    }}

    results = await MongoClient().find(r, limit)
    resp = {'results': tuple(results)}
    return web.Response(text=str(resp), status=200)


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8888)
