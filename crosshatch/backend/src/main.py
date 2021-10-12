from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

import socketio
import uuid
from urllib.parse import parse_qs

app = FastAPI()

# CORS
cors_allowed_origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SocketIO
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
sio_app = socketio.ASGIApp(sio)


user_list = []
rooms = {}


@sio.event
async def connect(sid, environ, auth):
    query_string = environ["QUERY_STRING"]
    room = parse_qs(query_string)["room"][0]
    print(f"connected to {sid} in {room}")
    user_list.append(sid)
    await sio.emit("updateUserList", user_list)


@sio.event
async def disconnect(sid):
    print(f"disconnected from {sid}")
    user_list.remove(sid)
    await sio.emit("updateUserList", user_list)


# Routes
@app.get("/")
def home():
    return "Hello, World!"


@app.get("/play/create/{puzzle_id}")
def create_room():
    room_id = str(uuid.uuid1())
    rooms[room_id] = puzzle_id
    response = RedirectResponse(url=f"/play/room/{room_id}")
    return response


# Mount SocketIO
app.mount("/", sio_app)
