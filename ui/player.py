from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import reactive

class Player(Vertical):
    def compose(self) -> ComposeResult:
        yield MediaPlayer()
        yield SongQueue()

class MediaPlayer(Vertical):

    def compose(self) -> ComposeResult:
        yield SongTitle(classes="text-center")
        yield SongStatus(classes="text-center")

class SongTitle(Widget):
    song_title = reactive("Song Titleeeeeeeeeeeeeeeeeeeeeeeeee")

    def render(self) -> str:
        if len(self.song_title) >= 23:
            return f"{self.song_title[:15]}..."
        return f"{self.song_title}"

class SongStatus(Widget):
    status = reactive("Paused")

    def render(self) -> str:
        return f"{self.status}"

class SongQueue(ScrollableContainer):
    def compose(self) -> ComposeResult:
        for i in range(16):
            if i == 7:
                yield QueuedSong(classes="queue-active")
            else:
                yield QueuedSong()

class QueuedSong(Widget):
    def compose(self) -> ComposeResult:
        yield Static("SONG QUEUED")
