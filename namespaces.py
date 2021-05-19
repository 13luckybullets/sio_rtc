from socketio import AsyncNamespace

from rtc.server_handler import RtcHandler


class Base(AsyncNamespace):

    async def on_connect(self, sid, environ):
        print(f'{sid} - connected')
        await self.emit('connection_response', {'data': 'Connected', 'count': 0}, room=sid)

    async def on_disconnect(self, sid):
        print(f'{sid} - Client disconnected')


class Rtc(Base):
    async def on_offer(self, sid, data):
        rtc = RtcHandler()

        await rtc.set_offer(data)
        answer = await rtc.get_answer()
        data = {
            'sdp': answer.sdp,
            'type': answer.type,
        }

        await rtc.recorder.start()
        await self.emit('answer', data)
