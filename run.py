
from aiopg.sa import create_engine
from aiohttp import web

from utils.config import load_config
from web.view import routes


async def init_db(app):
    config = app['config']['db']
    engine = await create_engine(**config)
    app['db'] = engine

async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()



async def init():
    app = web.Application()
    app['config'] = load_config()
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    app.add_routes(routes)
    return app
app = init()

web.run_app(app, host='0.0.0.0', port=8000)