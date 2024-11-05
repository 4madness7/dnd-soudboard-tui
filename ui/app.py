from textual.app import App, ComposeResult
from textual.containers import Horizontal

from ui.player import Player, SongStatus
from ui.playlists import Playlists
from ui.sound_effects import SoundEffects

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
                Playlists(classes="blue"),
                SoundEffects(),
            )

    def action_test(self) -> None:
        player = self.query_one(SongStatus)
        player.toggle_class("playing")
        if "playing" in player.classes:
            player.status = "Playing"
        else:
            player.status = "Paused"
