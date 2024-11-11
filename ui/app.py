from textual.app import App, ComposeResult
from textual.containers import Horizontal

from data import Data
from ui.input_file import InputFile
from ui.player import Player, SongQueue, SongStatus
from ui.playlists import Playlists
from ui.sound_effects import SoundEffects

class DNDSoundBoard(App):
    def __init__(self, data: Data):
        self.data = data
        super().__init__(None, None, False, False)

    CSS_PATH = "styles.tcss"
    # This allows to quit just by pressing q, I might have to change this later
    BINDINGS = [
            ("q", "quit", "Quit"),

            ("space", "test", "TEST"),
            ("ctrl+n", "toggle_input_file", "Open/close input file"),

            ("ctrl+q", "focus_queue", "Put focus on the queue pane"),
            # ("ctrl+p", "focus_playlist", "Put focus on the playlist pane"),
            # ("ctrl+s", "focus_soundboard", "Put focus on the soundboard pane"),
        ]

    def compose(self) -> ComposeResult:
        yield Horizontal(
                Player(),
                Playlists(data=self.data, classes="blue"),
                SoundEffects(),
                classes="l1"
            )
        yield InputFile(
                data=self.data,
                placeholder="Insert path here (press ENTER to submit)",
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

    def action_focus_queue(self) -> None:
        self.query_one(SongQueue).focus()

