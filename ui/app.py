from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import ContentSwitcher

from consts import MEDIA_PATH,PLAYLIST_PATH
from data import Data
from ui.add_playlist import AddPlaylist
from ui.edit_playlist import EditPlaylist
from ui.edit_soundboard import EditSoundBoard
from ui.input_file import InputFile
from ui.player import Player, SongQueue, SongStatus, SongTitle
from ui.playlists import Playlists
from ui.sound_effects import SoundEffects
import os, mpv

class DNDSoundBoard(App):
    def __init__(self, data: Data):
        self.data = data
        self.sb_player = mpv.MPV()
        self.curr_playlist = []
        self.pl_player = mpv.MPV(loop_playlist="inf")
        self.load_playlist()
        if len(self.pl_player.playlist_filenames) > 0:
            self.pl_player.playlist_play_index(0)
            self.pl_player.pause = True
        @self.pl_player.property_observer('playlist-pos')
        def _(_, i):
            # Here, _value is either None if nothing is playing or a float containing
            # fractional seconds since the beginning of the file.
            song_title = self.pl_player.playlist_filenames[i].split(os.sep)[-1].split(".")[0]
            self.app.query_one(SongTitle).song_title = song_title
        super().__init__(None, None, False, False)

    CSS_PATH = "styles.tcss"
    # This allows to quit just by pressing q, I might have to change this later
    BINDINGS = [
            ("q", "quit", "Quit"),

            ("space", "play_pause", "Play/pause current playlist"),
            ("ctrl+n", "toggle_input_file", "Open/close input file"),

            ("ctrl+q", "focus_queue", "Put focus on the queue pane"),
            Binding("ctrl+p", "focus_playlist", "Put focus on the playlist pane", priority=True),
            ("ctrl+s", "focus_soundboard", "Put focus on the soundboard pane"),
            ("ctrl+a", "add_playlist", "Add new playlist"),
            (">", "next_song", "Move to next song in playlist"),
            ("<", "prev_song", "Move to prev song in playlist"),
        ]

    def compose(self) -> ComposeResult:
        for s in self.data.soundboard:
            bind = Binding(self.data.soundboard[s], f"play_sound({s})", "play sound", show=False, priority=True)
            self._bindings._add_binding(bind)

        yield Horizontal(
                Player(player=self.pl_player),
                ContentSwitcher(
                    Playlists(data=self.data, id="playlists"),
                    AddPlaylist(data=self.data, id="add-playlist"),
                    EditPlaylist(data=self.data, id="edit-playlist"),
                    EditSoundBoard(data=self.data, id="edit-soundboard"),
                    classes="border-right-purple",
                    initial="playlists",
                ),
                SoundEffects(data=self.data),
                classes="l1"
            )
        yield InputFile(
                data=self.data,
                placeholder="Insert path here (press ENTER to submit)",
                classes="l2 none"
            )

    def load_playlist(self, refresh_player: bool = False):
        self.pl_player.playlist_clear()
        if len(self.pl_player.playlist_filenames) > 0:
            self.pl_player.playlist_remove()
        if os.path.exists(PLAYLIST_PATH):
            with open(PLAYLIST_PATH, "r") as file:
                lines = file.readlines()
                if len(lines) > 0:
                    for line in lines:
                        self.pl_player.playlist_append(line.strip())
        if refresh_player:
            self.query_one(Player).refresh(recompose=True)

    def action_play_sound(self, id: int):
        path = os.path.join(MEDIA_PATH, self.data.songs[id].file_name)
        self.sb_player.play(path)

    def action_play_pause(self) -> None:
        self.pl_player.pause = not self.pl_player.pause
        player = self.query_one(SongStatus)
        player.toggle_class("playing")
        if "playing" in player.classes:
            player.status = "Playing"
        else:
            player.status = "Paused"

    def action_next_song(self) -> None:
        if self.pl_player.playlist_pos == len(self.pl_player.playlist_filenames) - 1:
            self.pl_player.playlist_pos = 0
        else:
            self.pl_player.playlist_next()

    def action_prev_song(self) -> None:
        if self.pl_player.playlist_pos == 0:
            self.pl_player.playlist_pos = len(self.pl_player.playlist_filenames) - 1
        else:
            self.pl_player.playlist_prev()

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

