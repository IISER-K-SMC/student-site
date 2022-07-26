import fastapi
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from . import main
from . import smc_db

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main.router)


@app.on_event("startup")
def smc_db_startup():
    smc_db.get_connection()

@app.on_event("shutdown")
def smc_db_shutdown():
    smc_db.close_connection()

@app.on_event("startup")
async def db_startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['server.models']}
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def db_shutdown():
    await Tortoise.close_connections()
