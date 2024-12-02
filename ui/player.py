import os
from typing import Literal
from mpv import MPV
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer, Vertical
from textual.widget import Widget
from textual.widgets import Button, Label
from textual.reactive import reactive
from textual.events import Focus

class Player(Vertical):
    def __init__(self, *children: Widget, player: MPV,  name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.pl_player = player
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        yield MediaPlayer()
        yield SongQueue(player=self.pl_player)

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
    def __init__(self, *children: Widget, player: MPV, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.pl_player = player
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    BINDINGS = [
        Binding("down,j", "move_focus('down', 'short')", "Focus to next song", show=False),
        Binding("up,k", "move_focus('up', 'short')", "Focus to previous song", show=False),
        Binding("ctrl+down,ctrl+d", "move_focus('down', 'long')", "Focus to the 4th song after", show=False),
        Binding("ctrl+up,ctrl+u", "move_focus('up', 'long')", "Focus to the 4th song before", show=False),
    ]

    focused_child = 0

    def compose(self) -> ComposeResult:
        first_song = "No song loaded"
        if len(self.pl_player.playlist_filenames) > 0:
            i = 0
            for song in self.pl_player.playlist_filenames:
                song_name = song.split(os.sep)[-1].split(".")[0]
                if i == 0:
                    first_song = song_name
                    i += 1
                yield Button(song_name)
        else:
            yield Label("Playlist empty.")
        if self.parent:
            self.parent.query_one(SongTitle).song_title = first_song

    def _on_focus(self, event: Focus) -> None:
        self.children[self.focused_child].focus()
        return super()._on_focus(event)

    def action_move_focus(self, direction: Literal["up", "down"], skip: Literal["short", "long"]) -> None:
        state = self.query("Button")
        if len(state):
            jump = 0
            match (skip):
                case 'short':
                    jump = 1
                case 'long':
                    jump = 4
            match (direction):
                case 'down':
                    self.focused_child = (self.focused_child + jump) % len(state.nodes)
                case 'up':
                    self.focused_child = (self.focused_child - jump) % len(state.nodes)
            state.nodes[self.focused_child].focus()
