import sys

import aiohttp_cors
from aiohttp import web


from apis.handler import RouteHandler


app = web.Application()


async def setup_service(app):
    try:

        handler = RouteHandler()

        app.router.add_route("GET", "/get-class-time-table", handler.get_time_table)

        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True, expose_headers="*", allow_headers="*",
                )
            },
        )
        for route in list(app.router.routes()):
            cors.add(route)

    except Exception as err:
        sys.exit(1)


app.on_startup.append(setup_service)

web.run_app(app, port=8001)
