
from aiopg.sa import create_engine
from aiohttp import web

from web.view import routes


async def init_db(app):
    engine = await create_engine(user='dev',
                                  database='aiohttp_test',
                                  host='127.0.0.1',
                                  password='developer')
    app['db'] = engine

async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()



async def init():
    app = web.Application()

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    app.add_routes(routes)
    return app

web.run_app(init(), host='127.0.0.1', port=8000)