from textual.app import ComposeResult
from textual.containers import Grid, ScrollableContainer, Vertical
from textual.widgets import Button, Static

class Player(ScrollableContainer):
    def compose(self) -> ComposeResult:
        yield MediaPlayer()

class MediaPlayer(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Title of song", classes="text-center")
        yield Static("Currently playing", classes="text-center", id="media-player")
