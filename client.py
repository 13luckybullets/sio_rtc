import sys

import socketio
import asyncio

from rtc.client_handler import ClientRTC


loop = asyncio.get_event_loop()

HOST = 'http://127.0.0.1:8080'


sys.path.append(".")
sio = socketio.AsyncClient(reconnection=False)
CR = ClientRTC()


@sio.event()
def connect():
    print("I'm connected!", sio.sid)


@sio.event()
def connect_error(sid):
    print("The connection failed!")


@sio.event()
def disconnect():
    print("I'm disconnected!")


@sio.event(namespace='/rtc')
async def answer(data):
    print(f"Catch answer")
    await CR.set_answer(data)
    await CR.recorder.start()


async def run_client():
    filepath = input("Input path to file, or leave blank to stream from webcam: ")
    await sio.connect(HOST, )

    CR.set_media_player(filepath)
    CR.add_tracks()
    await CR.create_offer()

    offer = CR.pc.localDescription
    data = {
        'sdp': offer.sdp,
        'type': offer.type,
        # additional media data:
        'file_data': {
            'name': 'name_123',
            'filetype': 'some_best_type'
        }
    }
    await sio.emit('offer', data, namespace='/rtc')
    await sio.wait()


if __name__ == '__main__':
    try:
        loop.run_until_complete(run_client())

    except (KeyboardInterrupt, RuntimeError):
        pass
    finally:
        loop.run_until_complete(CR.pc.close())
        loop.close()
