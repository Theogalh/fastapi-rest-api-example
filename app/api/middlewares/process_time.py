import time
from starlette.types import ASGIApp, Scope, Receive, Send


class ProcessTimeMiddleWare:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        start_time = time.time()
        await self.app(scope, receive, send)
        if scope['type'] in ("http", "websocket"):
            process_time = time.time() - start_time
            headers = dict(scope["headers"])
            headers[b"X-Process-Time"] = str(process_time)
