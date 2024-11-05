from textual.app import App, ComposeResult
from textual.containers import Horizontal

from ui.input_file import InputFile
from ui.player import Player, SongStatus
from ui.playlists import Playlists
from ui.sound_effects import SoundEffects

class DNDSoundBoard(App):

    CSS_PATH = "styles.tcss"
    # This allows to quit just by pressing q, I might have to change this later
    BINDINGS = [
            ("q", "quit", "Quit"),

            ("space", "test", "TEST"),
            ("ctrl+n", "toggle_input_file", "Open/close input file"),
        ]

    def compose(self) -> ComposeResult:
        yield Horizontal(
                Player(),
                Playlists(classes="blue"),
                SoundEffects(),
                classes="l1"
            )
        yield InputFile(
                placeholder="Insert file path here (press ENTER to submit)",
                classes="l2 none"
            )

    def action_test(self) -> None:
        player = self.query_one(SongStatus)
        player.toggle_class("playing")
        if "playing" in player.classes:
            player.status = "Playing"
        else:
            player.status = "Paused"

    def action_toggle_input_file(self) -> None:
        input_file = self.query_one(InputFile)
        input_file.toggle_class("none")
        if not input_file.has_class("none"):
            input_file.focus()
