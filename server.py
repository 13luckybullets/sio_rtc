import socketio
from aiohttp import web

from namespaces import Base, Rtc

sio = socketio.AsyncServer(async_mode='aiohttp')


app = web.Application()
sio.attach(app)

sio.register_namespace(Base('/'))
sio.register_namespace(Rtc('/rtc'))


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)

