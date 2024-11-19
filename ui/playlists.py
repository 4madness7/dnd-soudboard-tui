from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.coordinate import Coordinate
from textual.widget import Widget
from textual.widgets import DataTable, Collapsible, _collapsible as clp
from textual.events import Focus
from textual.binding import Binding
from typing import Literal
from data import Data

class Playlists(ScrollableContainer):
    BINDINGS = [
        Binding("down,j", "move_focus('down', 'short')", "Focus to next song", show=False),
        Binding("up,k", "move_focus('up', 'short')", "Focus to previous song", show=False),
        Binding("ctrl+down,ctrl+d", "move_focus('down', 'long')", "Focus to the 4th song after", show=False),
        Binding("ctrl+up,ctrl+u", "move_focus('up', 'long')", "Focus to the 4th song before", show=False),
    ]

    focused_child = 0

    def __init__(self, data: Data, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        yield PlaylistCollapsible(
            self.data,
            list(self.data.songs.keys()),
            title="Saved audios",
            id="saved-audios",
        )

    def action_move_focus(self, direction: Literal["up", "down"], skip: Literal["short", "long"]) -> None:
        state = self.query(PlaylistCollapsibleTitle)
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


    def _on_focus(self, event: Focus) -> None:
        self.children[self.focused_child].children[0].focus()
        return super()._on_focus(event)


class PlaylistCollapsible(Collapsible):
    BINDINGS = [
        Binding("p", "move_focus_song('up')", "Focus to previous song in table", show=False),
        Binding("n", "move_focus_song('down')", "Focus to next song in table", show=False),
        # This is temporary (maybe)
        Binding("enter", "no_bind", "Removed binding", show=False, priority=True),
    ]

    def __init__(self, data: Data, to_render: list[int], *children: Widget, title: str = "Toggle", collapsed: bool = True, collapsed_symbol: str = "▶", expanded_symbol: str = "▼", name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(*children, title=title, collapsed=collapsed, collapsed_symbol=collapsed_symbol, expanded_symbol=expanded_symbol, name=name, id=id, classes=classes, disabled=disabled)
        self._title = PlaylistCollapsibleTitle(
            label=title,
            collapsed_symbol=collapsed_symbol,
            expanded_symbol=expanded_symbol,
            collapsed=collapsed,
        )
        self.data = data
        self._table = DataTable(cursor_type="row")
        self._table.styles.width = "100"
        self.col_key_name, _ = self._table.add_columns("Name".ljust(88), "Duration")
        for i in to_render:
            if len(self.data.songs[i].name) > 86:
                self._table.add_row(self.data.songs[i].name[:83]+"...", self.data.songs[i].duration)
            else:
                self._table.add_row(self.data.songs[i].name, self.data.songs[i].duration)
        self._table.sort(self.col_key_name, key=lambda name: name.lower())
        self.compose_add_child(self._table)

    def update_table(self):
        indexes = list(self.data.songs.keys())
        titles = list(map(lambda x: x.strip(), list(self._table.get_column(self.col_key_name))))
        for i in indexes:
            if self.data.songs[i].name not in titles:
                if len(self.data.songs[i].name) > 86:
                    self._table.add_row(self.data.songs[i].name[:83]+"...", self.data.songs[i].duration)
                else:
                    self._table.add_row(self.data.songs[i].name, self.data.songs[i].duration)

        self._table.sort(self.col_key_name, key=lambda name: name.lower())

    def action_move_focus_song(self, direction: Literal["up", "down"]) -> None:
        if self._table.row_count > 0:
            match (direction):
                case 'down':
                    new_row = (self._table.cursor_coordinate.row + 1) % len(self._table.rows)
                    self._table.cursor_coordinate = Coordinate(new_row, 0)
                case 'up':
                    new_row = (self._table.cursor_coordinate.row - 1) % len(self._table.rows)
                    self._table.cursor_coordinate = Coordinate(new_row, 0)

    def action_no_bind(self):
        pass

    def _on_focus(self, event: Focus) -> None:
        self.children[0].focus()
        return super()._on_focus(event)

class PlaylistCollapsibleTitle(clp.CollapsibleTitle):
    def watch_has_focus(self, value: bool) -> None:
        self.post_message(self.Toggle())
        return super().watch_has_focus(value)
