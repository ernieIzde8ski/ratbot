from asyncio import get_event_loop


def run(client, token):
    async def start():
        try:
            await client.start(token)
        except KeyboardInterrupt:
            await client.close()

    async def stop():
        await client.close()

    try:
        get_event_loop().run_until_complete(start())
    except KeyboardInterrupt:
        get_event_loop().run_until_complete(stop())
