from importlib import util

import asyncio

from nio import (AsyncClient, SyncResponse, RoomMessageText)
    
async_client = AsyncClient(
    "https://matrix.org", "USERNAME"
)

async def main():
    print('Starting ...')
    response = await async_client.login("PASSWORD", "")
    print(response)
    print('... Started!')

    while (True):
        sync_response = await async_client.sync(30000)
        print(sync_response)
    
    await async_client.close()
    
asyncio.run(main())