from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import socketio

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


@sio.event
async def connect(sid, environ, auth):
    print(f"connected to {sid}")
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


# Mount SocketIO
app.mount("/", sio_app)
