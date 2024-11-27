from textual.app import ComposeResult
from textual.containers import Vertical
from textual.coordinate import Coordinate
from textual.widgets import ContentSwitcher, DataTable
from textual.widget import Widget
from textual.binding import Binding
from textual.events import Focus
from typing import Literal

from data import Data
from ui.edit_soundboard import EditSoundBoard

COL_MAX_CHARS = 24
STR_MAX_CHARS = COL_MAX_CHARS - 3

class SoundEffects(Vertical):
    def __init__(self, data: Data, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    BINDINGS = [
        Binding("down,j", "move_focus('down')", "Focus sound under selected", show=False),
        Binding("up,k", "move_focus('up')", "Focus sound up selected", show=False),
        Binding("e", "open_edit", "Open edit panel", show=False),
    ]

    can_focus = True
    focused_row = 0

    def compose(self) -> ComposeResult:
        table = DataTable(cursor_type="none")
        self.col_key_name, _ = table.add_columns("Name".ljust(COL_MAX_CHARS), "Key")
        for key in self.data.soundboard:
            if len(self.data.songs[key].name) > COL_MAX_CHARS:
                table.add_row(self.data.songs[key].name[:STR_MAX_CHARS], self.data.soundboard[key])
            else:
                table.add_row(self.data.songs[key].name, self.data.soundboard[key])
        yield table

    def action_move_focus(self, move: Literal["up", "down"]) -> None:
        state = self.query_one(DataTable)
        if state.row_count > 0:
            match (move):
                case 'down':
                    new_row = (state.cursor_coordinate.row + 1) % len(state.rows)
                    state.cursor_coordinate = Coordinate(new_row, 0)
                case 'up':
                    new_row = (state.cursor_coordinate.row - 1) % len(state.rows)
                    state.cursor_coordinate = Coordinate(new_row, 0)

    def update_table(self):
        table = self.query_one(DataTable)
        indexes = self.data.soundboard.keys()
        titles = list(map(lambda x: x.strip(), list(table.get_column(self.col_key_name))))
        for i in indexes:
            new_title = self.data.songs[i].name
            if len(self.data.songs[i].name) > COL_MAX_CHARS:
                new_title = self.data.songs[i].name[:STR_MAX_CHARS]
            if new_title not in titles:
                table.add_row(new_title, self.data.soundboard[i])

        saved_titles = list(map(
                    lambda x: x if len(x) <= COL_MAX_CHARS else x[:STR_MAX_CHARS],
                    map(lambda x: self.data.songs[x].name.strip(), self.data.soundboard)
                ))

        for row in table.rows.copy():
            if table.get_row(row)[0] not in saved_titles:
                table.remove_row(row)
        table.sort(self.col_key_name, key=lambda name: name.lower())

    def action_open_edit(self):
        self.app.query_one(ContentSwitcher).current = "edit-soundboard"
        self.app.query_one(EditSoundBoard).focus()

    def watch_has_focus(self, value: bool) -> None:
        if value:
            self.query_one(DataTable).cursor_type = "row"
        else:
            self.query_one(DataTable).cursor_type = "none"
        return super().watch_has_focus(value)

    # def _on_focus(self, event: Focus) -> None:
    #     self.query_one(DataTable).focus()
    #     return super()._on_focus(event)
