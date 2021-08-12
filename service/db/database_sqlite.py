from configs.path_config import DATA_PATH
from tortoise import Tortoise


async def db_init():
    await Tortoise.init(
        db_url=f"sqlite://{DATA_PATH}data.db",
        modules={"models": ["service.db.model.models"]},
    )
    await Tortoise.generate_schemas()


async def db_disconnect():
    await Tortoise.close_connections()
