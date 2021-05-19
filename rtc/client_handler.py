from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer


class ClientRTC:
    offer = {}
    media_player = None

    def __init__(self):
        self.pc = RTCPeerConnection()
        self.recorder = MediaBlackhole()

    def set_media_player(self, filepath=None):
        if filepath:
            self.media_player = MediaPlayer(filepath)
        else:
            self.media_player = MediaPlayer(
                '/dev/video0',
                format='v4l2',
                options={
                    'video_size': '640x480'
                }
            )

    def add_tracks(self):
        if self.media_player and self.media_player.audio:
            self.pc.addTrack(self.media_player.audio)

        if self.media_player and self.media_player.video:
            self.pc.addTrack(self.media_player.video)

    async def create_offer(self):
        self.offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(self.offer)

    async def set_answer(self, data):
        answ = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
        await self.pc.setRemoteDescription(answ)
