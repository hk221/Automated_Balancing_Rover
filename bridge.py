import asyncio
import websockets
import socketio
import json

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("Connected to web server")

@sio.event
async def disconnect():
    print ("Disconnected from web server")

async def receive_message():
    async with websockets.connect('ws://172.20.10.2:3000') as websocket: #connect to triangulation code
        print ("connected to socket")
        while True:
            message = await websocket.recv()
            instruction = message.split(":")[0]
            payload = message.split(":")[1]
            print (payload)
            

            print ("Sending to site...")
            await sio.emit(instruction, {'x': 0, 'y': 0})  # Adjust the event name and data

            # Process the received message as needed

async def main():
    await sio.connect('http://172.20.10.2:3001')  # Replace with the appropriate URL of the other Socket.IO server
    await asyncio.gather(
        receive_message(),
        sio.wait()
    )
    await sio.disconnect()

asyncio.get_event_loop().run_until_complete(receive_message())
