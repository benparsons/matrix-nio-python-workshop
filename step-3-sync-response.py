from importlib import util
import pprint
pp = pprint.PrettyPrinter(indent=2)

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

        if len(sync_response.rooms.join) > 0:
            joins = sync_response.rooms.join
            for room_id in joins:
                pp.pprint(joins[room_id])
        key = input("Sync again?")
        if len(key) > 0:
            print("Closing connection ...")
            await async_client.close()
            print("... closed")
            exit()
    
    
    
asyncio.run(main())