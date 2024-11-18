from textual.containers import ScrollableContainer, Vertical
from textual.app import ComposeResult
from textual.widgets import Checkbox, Input, Label
from textual.widget import Widget
from textual.binding import Binding
from typing import Literal
from textual.events import Focus

from data import Data


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
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        yield Label("Playlist name (CTRL+f to toggle focus) ")
        yield Input(placeholder="Insert playlist name")
        yield Label("Choose songs")
        yield SongChecklist(data=self.data)

    def action_move_focus(self, direction: Literal["up", "down"], skip: Literal["short", "long"]) -> None:
        state = self.query(Checkbox)
        i = 0
        while not state.nodes[i].has_focus:
            if i >= len(state.nodes) - 1:
                break
            i += 1
        jump = 0
        match (skip):
            case 'short':
                jump = 1
            case 'long':
                jump = 4
        match (direction):
            case 'down':
                self.focused_child = (i + jump) % len(state.nodes)
            case 'up':
                self.focused_child = (i - jump) % len(state.nodes)
        state.nodes[self.focused_child].focus()

    def action_toggle_input(self) -> None:
        input = self.query_one(Input)
        if input.has_focus:
            state = self.query(Checkbox)
            state.nodes[self.focused_child].focus()
        else:
            input.focus()

    def _on_focus(self, event: Focus) -> None:
        state = self.query(Checkbox)
        state.nodes[self.focused_child].focus()
        return super()._on_focus(event)


class SongChecklist(ScrollableContainer):
    def __init__(self, data: Data, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        match = list(map(lambda kv: (kv[0], kv[1].name.lower()), self.data.songs.items()))
        match = sorted(match, key=lambda kv: kv[1])

        indexes = map(lambda kv: kv[0], match)

        for i in indexes:
            yield Checkbox(self.data.songs[i].name)
