from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .models.crossword import Crossword

import socketio
import uuid
from urllib.parse import parse_qs
import puz
import itertools as it
from collections import defaultdict

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


# temporary
puzzles = {
    "abcd": Crossword("abcd", "WSJ 10/09/2021", "wsj211009"),
    "efgh": Crossword("efgh", "WSJ 10/11/2021", "wsj211011"),
    "zxyz": Crossword("zxyz", "WSJ 10/12/2021", "wsj211012"),
}


@sio.event
async def connect(sid, environ, auth):
    query_string = environ["QUERY_STRING"]
    room = parse_qs(query_string)["room"][0]
    sio.enter_room(sid, room)
    await sio.emit("crosswordInit", room_data[room], room=sid)


@sio.event
async def disconnect(sid):
    pass


# Routes
@app.get("/")
def home():
    return "Hello, World!"


@app.get("/puzzles")
def get_puzzles():
    # TODO only return the necessary information we want to display
    return list(puzzles.values())


room_data = {}


@app.get("/play/create/{puzzle_id}")
def create_room(puzzle_id):
    room_code = str(uuid.uuid1())
    room_path = f"/play/room/{room_code}"
    room_data[room_path] = get_puzzle_data(puzzle_id)
    return room_path


def get_puzzle_data(puzzle_id):
    puzzle = puz.read(f"src/resources/{puzzles[puzzle_id].filename}.puz")

    grid = [
        [
            "#" if puzzle.fill[col + row * puzzle.width] == "." else ""
            for col in range(puzzle.width)
        ]
        for row in range(puzzle.height)
    ]

    numbering = puzzle.clue_numbering()
    clues = [
        {}
        for _ in range(
            max(clue["num"] for clue in [*numbering.down, *numbering.across]) + 1
        )
    ]
    clues[0] = None
    index_to_nums = defaultdict(lambda: {"down": None, "across": None})
    clue_grid = [
        [None if val == "#" else {"down": None, "across": None} for val in row]
        for row in grid
    ]

    for clue, direction in [
        *zip(numbering.down, it.repeat("down")),
        *zip(numbering.across, it.repeat("across")),
    ]:
        num, flat_index, clue = clue["num"], clue["cell"], clue["clue"]
        clues[num][direction] = clue

        start_r, start_c = flat_index // puzzle.width, flat_index % puzzle.width
        clues[num]["start_r"] = start_r
        clues[num]["start_c"] = start_c
        index_to_nums[(start_r, start_c)][direction] = num

    for r, row in enumerate(clue_grid):
        for c, clue_dict in enumerate(row):
            if clue_dict is None:
                continue
            cur_r, cur_c = r + 1, c
            while clue_dict["down"] is None:
                cur_r -= 1
                clue_dict["down"] = index_to_nums[(cur_r, cur_c)]["down"]
            cur_r, cur_c = r, c + 1
            while clue_dict["across"] is None:
                cur_c -= 1
                clue_dict["across"] = index_to_nums[(cur_r, cur_c)]["across"]

    data = {
        "grid": grid,
        "width": puzzle.width,
        "height": puzzle.height,
        "clues": clues,
        "clue_grid": clue_grid,
    }
    return data


# Mount SocketIO
app.mount("/", sio_app)
