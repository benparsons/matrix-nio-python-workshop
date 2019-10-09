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
    
    await async_client.close()
    
asyncio.run(main())