from textual.app import ComposeResult
from textual.containers import Vertical
from textual.coordinate import Coordinate
from textual.widgets import DataTable
from textual.binding import Binding
from textual.events import Focus
from typing import Literal

class SoundEffects(Vertical):
    BINDINGS = [
        Binding("down,j", "move_focus('down')", "Focus sound under selected", show=False),
        Binding("up,k", "move_focus('up')", "Focus sound up selected", show=False),
    ]

    can_focus = True
    focused_row = 0

    def compose(self) -> ComposeResult:
        table = DataTable(cursor_type="none")
        table.add_columns("Key", "Name".ljust(24))
        for i in range(40):
            table.add_row(f"{i}","Song name")
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


    def _on_focus(self, event: Focus) -> None:
        self.query_one(DataTable).cursor_type = "row"
        return super()._on_focus(event)
