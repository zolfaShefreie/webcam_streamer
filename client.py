import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, Gtk

class GTK_Main:

    def __init__(self):
        self.first = True
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Videotestsrc-Player")
        self.window.set_default_size(300, -1)
        self.window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        self.window.add(vbox)
        self.button = Gtk.Button("Start")
        self.button2 = Gtk.Button("Play")
        self.button.connect("clicked", self.start_stop)
        self.button2.connect("clicked", self.play_puase)
        vbox.add(self.button)
        vbox.add(self.button2)
        self.window.show_all()
        self.player = Gst.parse_launch(
            "rtspsrc name=source latency=0 ! decodebin ! queue ! videoconvert ! autovideosink name=sink async=false")

        source = self.player.get_by_name("source")
        self.sink = self.player.get_by_name("sink")
        source.props.location = "rtsp://localhost:8554/stream1"

    def play_puase(self, w):
        if self.button2.get_label() == "Play":
            self.button2.set_label("Pause")
            print(self.player.set_state(Gst.State.PLAYING))  
            
        else:
            print(self.player.set_state(Gst.State.PAUSED))
            self.button2.set_label("Play")
            self.first = False

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            print(self.player.set_state(Gst.State.READY))
            
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            self.window.destroy()

GObject.threads_init()
Gst.init(None)        
GTK_Main()
Gtk.main()
