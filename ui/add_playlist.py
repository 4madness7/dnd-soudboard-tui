from rich.console import RenderableType
from rich.text import TextType
from textual.containers import Grid, ScrollableContainer, Vertical
from textual.app import ComposeResult
from textual.widgets import Checkbox, Input, Label
from textual.widget import Widget
from textual.binding import Binding
from typing import Literal
from textual.events import Focus

from data import Data
from ui.playlists import Playlists
import pickle
from consts import DATA_PATH


class AddPlaylist(Vertical):
    BINDINGS = [
        Binding("down,j", "move_focus('down', 'short')", "Focus to next song", show=False),
        Binding("up,k", "move_focus('up', 'short')", "Focus to previous song", show=False),
        Binding("ctrl+down,ctrl+d", "move_focus('down', 'long')", "Focus to the 4th song after", show=False),
        Binding("ctrl+up,ctrl+u", "move_focus('up', 'long')", "Focus to the 4th song before", show=False),
        Binding("ctrl+f", "toggle_input", "Toggle focus to title text input", show=False, priority=True),
    ]

    can_focus = True

    focused_child = 0

    def __init__(self, data: Data, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        self.new_playlist = []
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        yield Label("Playlist name ([b]CTRL+f[/b] to toggle focus, [b]enter[/b] while focused to submit) ")
        yield NameInput(placeholder="Insert playlist name")
        yield Grid(
            Label("New playlist", classes="label-20"),
            Label("Choose songs"),
            PlaylistList(data=self.data, new_playlist=self.new_playlist),
            SongChecklist(data=self.data, new_playlist=self.new_playlist),
            classes="add-playlist-grid"
        )

    def action_move_focus(self, direction: Literal["up", "down"], skip: Literal["short", "long"]) -> None:
        state = self.query(Checkbox)
        if len(state.nodes) > 0:
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

    def action_toggle_input(self) -> None:
        input = self.query_one(Input)
        if input.has_focus:
            state = self.query(Checkbox)
            if len(state.nodes) > 0:
                state.nodes[self.focused_child].focus()
        else:
            input.focus()

    def create_playlist(self):
        input = self.query_one(NameInput)
        if input.value == "":
            self.notify("Please insert playlist name", severity="error")
            return
        if len(self.new_playlist) == 0:
            self.notify("Please insert at least one song to the playlist", severity="error")
            return
        self.data.playlists[input.value.strip()] = self.new_playlist.copy()
        pickle.dump(self.data, open(DATA_PATH, 'wb'))
        self.new_playlist = []
        self.refresh(recompose=True)
        self.app.query_one(Playlists).refresh(recompose=True)
        self.notify(f"Playlist '{input.value}' added")

    def _on_focus(self, event: Focus) -> None:
        state = self.query(Checkbox)
        if len(state.nodes) > 0:
            state.nodes[self.focused_child].focus()
        return super()._on_focus(event)

class NameInput(Input):
    async def action_submit(self) -> None:
        if type(self.parent) is AddPlaylist:
            self.parent.create_playlist()
        return await super().action_submit()

class PlaylistList(Widget):
    def __init__(self, data: Data, new_playlist, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        self.new_playlist = new_playlist
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        for i in range(len(self.new_playlist)):
            yield Label(f"{i+1}. {self.data.songs[self.new_playlist[i]].name}")

class SongChecklist(ScrollableContainer):
    def __init__(self, data: Data, new_playlist, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        self.new_playlist = new_playlist
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        match = list(map(lambda kv: (kv[0], kv[1].name.lower()), self.data.songs.items()))
        match = sorted(match, key=lambda kv: kv[1])

        indexes = map(lambda kv: kv[0], match)

        for i in indexes:
            yield SongCheckbox(
                new_playlist=self.new_playlist,
                song_id=i,
                label=self.data.songs[i].name
            )

class SongCheckbox(Checkbox):
    def __init__(self, new_playlist, song_id: int, label: TextType = "", value: bool = False, button_first: bool = True, *, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False, tooltip: RenderableType | None = None) -> None:
        self.new_playlist: list[int] = new_playlist
        self.song_id = song_id
        super().__init__(label, value, button_first, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)

    def watch_value(self) -> None:
        if self.value:
            self.new_playlist.append(self.song_id)
        else:
            self.new_playlist.remove(self.song_id)

        if self.app:
            self.app.query(PlaylistList).refresh(recompose=True)
        return super().watch_value()
