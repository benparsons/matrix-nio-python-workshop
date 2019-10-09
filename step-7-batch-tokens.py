from importlib import util
import pprint
pp = pprint.PrettyPrinter(indent=2)

import asyncio

from nio import (AsyncClient, SyncResponse, RoomMessageText)
    
async_client = AsyncClient(
    "https://matrix.org", "USERNAME"
)

response_string = "!replybot"
next_batch = ""

async def main():
    print('Starting ...')
    response = await async_client.login("PASSWORD", "")
    print(response)
    print('... Started!')
    with open ("next_batch","r") as next_batch_token:
        async_client.next_batch = next_batch_token.read()
    
    while (True):
        sync_response = await async_client.sync(30000)
        with open("next_batch","w") as next_batch_token:
            next_batch_token.write(sync_response.next_batch)

        if len(sync_response.rooms.join) > 0:
            joins = sync_response.rooms.join
            for room_id in joins:
                for event in joins[room_id].timeline.events:
                    if isinstance(event, RoomMessageText):
                        print(event)
                        if event.body.startswith(response_string):
                            response_body = event.body.replace(response_string, "")
                            response_body = response_body.strip()
                            content = {
                                "body": response_body,
                                "msgtype": "m.text"
                            }
                            await async_client.room_send(room_id, 'm.room.message', content)

        key = input("Sync again?")
        if len(key) > 0:
            print("Closing connection ...")
            await async_client.close()
            print("... closed")
            exit()
    
    
    
asyncio.run(main())