import asyncio
import random
import string

import aiohttp


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(string_length))


async def post_user(queue):
    async with aiohttp.ClientSession() as session:
        while True:
            data = await queue.get()
            async with session.post('http://127.0.0.1:8888/users', json=data) as response:
                resp = await response.text()
                print(resp)
            queue.task_done()


async def main():
    parallel = 100
    queue = asyncio.Queue()

    for _ in range(7000000):
        data = {"name": random_string(), "lon": random.uniform(-180, 180), "lat": random.uniform(-90, 90)}
        await queue.put(data)

    for _ in range(parallel):
        asyncio.create_task(post_user(queue))

    await queue.join()


if __name__ == '__main__':
    asyncio.run(main())
