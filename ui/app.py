from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import ContentSwitcher

from data import Data
from ui.add_playlist import AddPlaylist
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
            Binding("ctrl+p", "focus_playlist", "Put focus on the playlist pane", priority=True),
            ("ctrl+s", "focus_soundboard", "Put focus on the soundboard pane"),
            ("ctrl+a", "add_playlist", "Add new playlist"),
        ]

    def compose(self) -> ComposeResult:
        yield Horizontal(
                Player(),
                ContentSwitcher(
                    Playlists(data=self.data, id="playlists"),
                    AddPlaylist(data=self.data, id="add-playlist"),
                    classes="blue",
                    initial="playlists",
                ),
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

    def action_focus_playlist(self) -> None:
        self.query_one(ContentSwitcher).current = "playlists"
        self.query_one(Playlists).focus()

    def action_focus_soundboard(self) -> None:
        self.query_one(SoundEffects).focus()

    def action_add_playlist(self) -> None:
        self.query_one(ContentSwitcher).current = "add-playlist"
        self.query_one(AddPlaylist).focus()

