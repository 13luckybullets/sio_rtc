import os

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRecorder

from utils import helper


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')


class RtcHandler:
    offer = None
    answer = None
    output_path = f"{BASE_DIR}/media/"

    def __init__(self):
        self.pc = RTCPeerConnection()
        self._file_path = self._get_file_path()
        self.recorder = MediaRecorder(self._file_path)
        self._pc_initialize()
        print(self._file_path)

    def _get_file_path(self):
        name = helper.get_rand_name()
        return f"{self.output_path}{name}.mp4"

    async def set_offer(self, data):
        self.offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
        await self.pc.setRemoteDescription(self.offer)

    async def get_answer(self):
        self.answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(self.answer)
        return self.pc.localDescription

    def _pc_initialize(self):
        pc = self.pc

        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                if isinstance(message, str) and message.startswith("ping"):
                    channel.send("pong" + message[4:])

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print("Connection state is %s", pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()

        @pc.on("track")
        async def on_track(track):
            print(f"Track {track.kind} received")
            self.recorder.addTrack(track)

            @track.on("ended")
            async def on_ended():
                print("Track %s ended", track.kind)
                await self.recorder.stop()
