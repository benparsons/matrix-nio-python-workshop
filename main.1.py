# * login, get response
# * get into a /sync loop
# * explore the sync response object
#   * maybe explore use of filters here
# * focus on `sync_response.rooms.join`
# * explore event objects
# * isolate specific message event objects
# * use `room_send`
# * use of /sync next_batch tokens

# the next section (not covered in this file)
# is to pass the message string to TensorFlow
# for sentiment analysis, then pass a number
# back

from importlib import util

import asyncio

from nio import (AsyncClient, SyncResponse)

from tfpredictor import TFPredictor
    
async_client = AsyncClient(
    "https://matrix.bpulse.org", "replybot"
)

response_string = "!replybot"
next_batch = ""
tfpredictor = TFPredictor(2)

async def main():    
    print('Hello ...')
    response = await async_client.login("password", "niotest")
    print(response)
    print('... World!')
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
                    if hasattr(event, 'body') and event.body.startswith(response_string):
                        print(event)

                        response_body = event.body.replace(response_string, "")
                        response_body = response_body.strip()
                        response_body = tfpredictor.predict(response_body.split())
                        content = {
                           "body": response_body,
                           "msgtype": "m.text"
                        }
                        await async_client.room_send(room_id, 'm.room.message', content)
 

    await async_client.close()
    

asyncio.run(main())