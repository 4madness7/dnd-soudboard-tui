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
        table = DataTable(cursor_type="row")
        table.styles.width = "100"
        table.add_columns("Name", "Duration")
        for song in self.data.songs:
            if len(song.name) > 86:
                table.add_row(song.name[:83]+"...", song.duration)
            else:
                table.add_row(song.name, song.duration)

        yield PlaylistCollapsible(table, title="Saved audios")

    def action_move_focus(self, direction: Literal["up", "down"], skip: Literal["short", "long"]) -> None:
        state = self.query(PlaylistCollapsibleTitle)
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


    def _on_focus(self, event: Focus) -> None:
        self.children[self.focused_child].children[0].focus()
        return super()._on_focus(event)


class PlaylistCollapsible(Collapsible):
    BINDINGS = [
        Binding("p", "move_focus_song('up')", "Focus to previous song in table", show=False),
        Binding("n", "move_focus_song('down')", "Focus to next song in table", show=False),
    ]

    def __init__(self, *children: Widget, title: str = "Toggle", collapsed: bool = True, collapsed_symbol: str = "▶", expanded_symbol: str = "▼", name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(*children, title=title, collapsed=collapsed, collapsed_symbol=collapsed_symbol, expanded_symbol=expanded_symbol, name=name, id=id, classes=classes, disabled=disabled)
        self._title = PlaylistCollapsibleTitle(
            label=title,
            collapsed_symbol=collapsed_symbol,
            expanded_symbol=expanded_symbol,
            collapsed=collapsed,
        )

    def action_move_focus_song(self, direction: Literal["up", "down"]) -> None:
        table = self.query_one(DataTable)
        match (direction):
            case 'down':
                new_row = (table.cursor_coordinate.row + 1) % len(table.rows)
                table.cursor_coordinate = Coordinate(new_row, 0)
            case 'up':
                new_row = (table.cursor_coordinate.row - 1) % len(table.rows)
                table.cursor_coordinate = Coordinate(new_row, 0)

    def _on_focus(self, event: Focus) -> None:
        self.children[0].focus()
        return super()._on_focus(event)

class PlaylistCollapsibleTitle(clp.CollapsibleTitle):
    def watch_has_focus(self, value: bool) -> None:
        self.post_message(self.Toggle())
        return super().watch_has_focus(value)
