from typing import List
import time
import random

import cv2
import base64
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get():
    return "HTMLResponse(html)"


@app.websocket("/xyz")
async def websocket_endpoint(websocket: WebSocket):
    # path = "/Users/haider/Desktop/cock_video.mp4"
    # cap = cv2.VideoCapture(path)

    await websocket.accept()
    print("connected")

    # try:
    #     while True:
    #         msg = await websocket.receive_text()

    #         print(msg)
    #         await websocket.send_json({"message": msg})
    # except Exception as e:
    #     print(f"{e=}")

    try:
        while True:

            data = await websocket.receive_text()
            print("data", data)
            data_json = json.loads(data)
            print("\ndata_json ", data_json)

            packet_no = data_json.get('packet_no')
            audio_bytes = data_json.get('audio_bytes')

            print("type of : ", type(audio_bytes))
            print("\npackent_no : ", packet_no)
            print("\naudio_bytes: ", audio_bytes)

            if audio_bytes == 'EOS':
                await websocket.send_json({"message": "200"})
                print("closing the websocket")
                await websocket.close()
                return
                
            else:
                print("In else condition")
                audio_bytes = base64.b64decode(
                        data_json.get('audio_bytes'))
                print("\naudio_bytes : ", audio_bytes)
                print(f"Received packet no: {packet_no}")

                with open('audio_output.mp3', 'wb') as f:
                        f.write(audio_bytes)

    except Exception as e:
            print(f"Exception: {e}")



