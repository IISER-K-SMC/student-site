import fastapi
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from . import smc_db_aio

from . import main
from . import security

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main.router)
app.include_router(security.router)


@app.on_event("startup")
async def db_startup():
    await smc_db_aio.get_pool()


    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['server.models']}
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def db_shutdown():
    await smc_db_aio.close_pool()

    await Tortoise.close_connections()
