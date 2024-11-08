from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widget import Widget
from textual.widgets import DataTable, Collapsible
from data import Data

class Playlists(ScrollableContainer):
    def __init__(self, data: Data, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        with Collapsible(title="Saved audios", collapsed=False):
            table = DataTable(cursor_type="row")
            table.styles.width = "90%"
            table.add_columns("Name", "Duration")
            for song in self.data.songs:
                table.add_row(song.name, song.duration)

            yield table

