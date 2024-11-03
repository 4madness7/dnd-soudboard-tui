from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer

from ui.player import Player, SongStatus

class DNDSoundBoard(App):

    CSS_PATH = "styles.tcss"
    # This allows to quit just by pressing q, I might have to change this later
    BINDINGS = [
            ("q", "quit", "Quit"),
            ("space", "test", "TEST"),
        ]

    def compose(self) -> ComposeResult:
        yield Horizontal(
                Player(),
                ScrollableContainer(classes="blue"),
                ScrollableContainer(classes="pink"),
                ScrollableContainer(),
            )

    def action_test(self) -> None:
        player = self.query_one(SongStatus)
        player.toggle_class("playing")
        if "playing" in player.classes:
            player.status = "Playing"
        else:
            player.status = "Paused"
