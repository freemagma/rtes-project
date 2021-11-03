from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .models.crossword import Crossword

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

# temporary, eventually load from database
crosswords = [
    "wsj211009",
    "wsj211011",
    "wsj211012",
]
crosswords_metadata = [ { "id": crossword, "name": Crossword.get_title_from_filename(crossword) } for crossword in crosswords ]

room_data = {}

@sio.on("crosswordEdit")
async def update_crossword(sid, data):
    print(data)

# Routes
@app.get("/")
def home():
    return "Hello, World!"

@app.get("/puzzles")
def get_puzzles():
    # TODO this is bad
    print(crosswords_metadata)
    return crosswords_metadata

# TODO puzzle_id is just the filename for now, we need to change this in the future when we add metadata to the filename
@app.get("/play/create/{puzzle_id}")
def create_room(puzzle_id):
    room_code = str(uuid.uuid4())
    room_path = f"/play/room/{room_code}" # TODO this is bad
    room_data[room_path] = Crossword(puzzle_id, room_code)
    return room_path

# Socket Events
@sio.event
async def connect(sid, environ, auth):
    query_string = environ["QUERY_STRING"]
    room = parse_qs(query_string)["room"][0]
    sio.enter_room(sid, room)
    await sio.emit("crosswordInit", room_data[room].get_puzzle_data(), room=sid)

@sio.event
async def disconnect(sid):
    pass

# Mount SocketIO
app.mount("/", sio_app)
