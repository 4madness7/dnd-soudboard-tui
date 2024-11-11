from typing import Literal
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer, Vertical
from textual.widget import Widget
from textual.widgets import Button
from textual.reactive import reactive
from textual.events import Focus

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
    BINDINGS = [
        Binding("down,j", "move_focus('down')", "Focus to next song", show=False),
        Binding("up,k", "move_focus('up')", "Focus to previous song", show=False),
    ]

    focused_child = 0

    def compose(self) -> ComposeResult:
        for i in range(16):
            if i == 7:
                yield Button("SONG QUEUED", classes="queue-active")
            else:
                yield Button("SONG QUEUED")

    def _on_focus(self, event: Focus) -> None:
        self.children[self.focused_child].focus()
        return super()._on_focus(event)

    def action_move_focus(self, direction: Literal["up", "down"] ) -> None:
        state = self.query("Button")
        i = 0
        while not state.nodes[i].has_focus:
            if i >= len(state.nodes) - 1:
                break
            i += 1
        match (direction):
            case 'down':
                self.focused_child = (i + 1) % len(state.nodes)
            case 'up':
                self.focused_child = (i - 1) % len(state.nodes)
        state.nodes[self.focused_child].focus()
