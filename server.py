import os
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import GObject, Gst, GstRtspServer, GLib

loop = GLib.MainLoop()
Gst.init(None)


class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        # ll = "videotestsrc is -live = 1 ! x264enc speed-preset = ultrafast tune = zerolatency ! rtph264pay name = pay0 pt = 96"
        # src_demux = "filesrc location=./test.mp4 ! qtdemux name=demux"
        # h264_transcode = "demux.video_0"
        # pipeline = "{0} {1} ! queue ! rtph264pay name=pay0 config-interval=1 pt=96".format(src_demux, h264_transcode)
        pipeline = "ksvideosrc device-index = 0 ! decodebin ! videoconvert ! x264enc ! rtph264pay pt = 96 name = pay0 "
        return Gst.parse_launch(pipeline)


class GstreamerRtspServer():
    def __init__(self):
        self.rtspServer = GstRtspServer.RTSPServer()
        self.rtspServer.set_address('localhost')
        self.rtspServer.set_service("8554")
        self.rtspServer.connect("client-connected", self.client_connected)
        print(self.rtspServer.get_address())
        factory = TestRtspMediaFactory()
        factory.set_shared(True)
        factory.set_transport_mode(GstRtspServer.RTSPTransportMode.PLAY)
        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory("/stream1", factory)
        self.rtspServer.attach(None)

    def client_connected(self, arg1, client):
        print('Client connected')
        # print(client)
        # print(client.get_connection())
        # print(client.get_session_pool())
        

if __name__ == '__main__':
    s = GstreamerRtspServer()
    loop.run()
