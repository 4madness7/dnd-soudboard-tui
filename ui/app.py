from textual.app import App, ComposeResult
from textual.containers import Horizontal

from textual.driver import Driver
from textual.types import CSSPathType
from typing import Type

from data import Data
from ui.input_file import InputFile
from ui.player import Player, SongStatus
from ui.playlists import Playlists
from ui.sound_effects import SoundEffects

class DNDSoundBoard(App):
    def __init__(self, data: Data, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False, ansi_color: bool = False):
        self.data = data
        super().__init__(driver_class, css_path, watch_css, ansi_color)

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
                Playlists(data=self.data, classes="blue"),
                SoundEffects(),
                classes="l1"
            )
        yield InputFile(
                data=self.data,
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
