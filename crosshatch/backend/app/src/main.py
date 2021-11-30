from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.models.crossword import Crossword
from src.api.api import api_router

import socketio
import uuid
import os
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

room_data = {}

# Routes
@app.get("/")
def home():
    return "Hello, World!"


@app.get("/puzzles")
def get_puzzles():
    # TODO this is bad
    # eventually load from database
    return [
        {"id": filename, "name": Crossword.get_title_from_filename(filename)}
        for filename in os.listdir("src/resources/")
    ]


# TODO puzzle_id is just the filename for now, we need to change this in the future when we add metadata to the filename
@app.get("/play/create/{puzzle_id}")
def create_room(puzzle_id):
    room_code = str(uuid.uuid4())
    room_path = f"/play/room/{room_code}"  # TODO this is bad
    room_data[room_path] = Crossword(puzzle_id, room_code)
    return room_path


# Socket Events
@sio.event
async def connect(sid, environ):
    query_string = environ["QUERY_STRING"]
    room = parse_qs(query_string)["room"][0]
    sio.enter_room(sid, room)
    await sio.emit("crosswordInit", room_data[room].get_puzzle_data(), room=sid)


@sio.event
async def disconnect(sid):
    pass


@sio.on("crosswordEdit")
async def update_crossword(sid, data):
    room_path, row, column, character = data.values()
    crossword = room_data[room_path]
    crossword.set_grid_cell(row, column, character)
    # TODO Only send message to everyone in room but creator (or the creator just discards the event)
    await sio.emit("crosswordUpdate", data, room=room_path)

app.include_router(api_router)

# Mount SocketIO
app.mount("/", sio_app)
