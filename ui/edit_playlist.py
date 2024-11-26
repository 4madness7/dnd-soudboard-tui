from typing import Literal
from textual.containers import Horizontal, Vertical
from textual.coordinate import Coordinate
from textual.reactive import reactive
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import data_table as dt, DataTable, Label
from textual.binding import Binding
from textual.events import Focus
import pickle

from consts import DATA_PATH
from data import Data

class EditPlaylist(Vertical):
    BINDINGS = [
        Binding("j", "move_focus('down')", "Move down to next table", show=False),
        Binding("k", "move_focus('up')", "Move up to next table", show=False),
        Binding("S", "save", "Save changes", show=False)
    ]

    def __init__(self, data: Data,*children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        self.playlist_name = list(self.data.playlists.keys())[0]
        self.playlist = []
        self.focused_child = 0
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    can_focus = True

    def compose(self) -> ComposeResult:
        self.playlist = self.data.playlists[self.playlist_name].copy()

        yield Horizontal(
            Label(f"CurrentPlaylist: [b]{self.playlist_name}[/b] |"),
            SaveStatus(),
            classes="w-100"
        )

        table = CurrentPlaylist(cursor_type="none", data=self.data ,playlist=self.playlist)
        table.add_column("Song name".ljust(97))
        for id in self.playlist:
            if len(self.data.songs[id].name) > 97:
                table.add_row((self.data.songs[id].name[:94]), key=id)
            else:
                table.add_row((self.data.songs[id].name), key=id)
        yield table

        yield Label("Available Songs")
        remaining_songs = list(set(self.data.songs.keys()) - set(self.playlist))
        table = AvailableSongs(cursor_type="none", data=self.data, playlist=self.playlist)
        col_key_name = table.add_column("Song name".ljust(97))
        for id in remaining_songs:
            if len(self.data.songs[id].name) > 97:
                table.add_row((self.data.songs[id].name[:94]), key=id)
            else:
                table.add_row((self.data.songs[id].name), key=id)
        table.sort(col_key_name, key=lambda name: name.lower())
        yield table

    def load_playlist(self, playlist_name: str):
        self.playlist_name = playlist_name

    def check_change(self):
        self.query_one(SaveStatus).changes = self.data.playlists[self.playlist_name] != self.playlist

    def refresh_playlist_table(self):
        collapsibles = self.app.query_one("Playlists").query("PlaylistCollapsible")
        for collap in collapsibles:
            if collap.playlist_name == self.playlist_name:
                collap.update_table()

    def action_save(self):
        status = self.query_one(SaveStatus)
        if status.changes:
            self.data.playlists[self.playlist_name] = self.playlist.copy()
            pickle.dump(self.data, open(DATA_PATH, 'wb'))
            self.refresh_playlist_table()
            self.notify("Changes saved.")
        else:
            self.notify("No changes found, skipping.", severity="warning")
        self.check_change()

    def action_move_focus(self, move: Literal["up", "down"]):
        tables = self.query(DataTable)
        match (move):
            case "up":
                self.focused_child = (self.focused_child + 1) % len(tables)
            case "down":
                self.focused_child = (self.focused_child - 1) % len(tables)
        tables[self.focused_child].focus()

    def _on_focus(self, event: Focus) -> None:
        self.query(DataTable)[self.focused_child].focus()
        return super()._on_focus(event)

class SaveStatus(Widget):
    changes = reactive(False)

    def render(self) -> str:
        self.remove_class("save-warning")
        if self.changes:
            self.add_class("save-warning")
            return "There are unsaved changes."
        return "Saved."

class PlaylistTable(DataTable):
    BINDINGS = [
        Binding("p", "move_focus('up')", "Focus to previous song in table", show=False),
        Binding("n", "move_focus('down')", "Focus to next song in table", show=False),
    ]

    def action_move_focus(self, move: Literal['up', 'down']):
        if self.row_count > 0:
            match (move):
                case 'down':
                    new_row = (self.cursor_coordinate.row + 1) % len(self.rows)
                    self.cursor_coordinate = Coordinate(new_row, 0)
                case 'up':
                    new_row = (self.cursor_coordinate.row - 1) % len(self.rows)
                    self.cursor_coordinate = Coordinate(new_row, 0)

    def watch_has_focus(self, value: bool) -> None:
        if value:
            self.cursor_type = "row"
        else:
            self.cursor_type = "none"
        return super().watch_has_focus(value)

    def find_key(self, row: int):
        return self._row_locations.get_key(row)


class CurrentPlaylist(PlaylistTable):
    def __init__(self, *, data: Data,playlist, show_header: bool = True, show_row_labels: bool = True, fixed_rows: int = 0, fixed_columns: int = 0, zebra_stripes: bool = False, header_height: int = 1, show_cursor: bool = True, cursor_foreground_priority: Literal["renderable", "css"] = "css", cursor_background_priority: Literal["renderable", "css"] = "renderable", cursor_type: dt.CursorType = "cell", cell_padding: int = 1, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.playlist: list[int] =  playlist
        self.data = data
        super().__init__(show_header=show_header, show_row_labels=show_row_labels, fixed_rows=fixed_rows, fixed_columns=fixed_columns, zebra_stripes=zebra_stripes, header_height=header_height, show_cursor=show_cursor, cursor_foreground_priority=cursor_foreground_priority, cursor_background_priority=cursor_background_priority, cursor_type=cursor_type, cell_padding=cell_padding, name=name, id=id, classes=classes, disabled=disabled)

    BINDINGS = [
        Binding("N", "move_row('down')", "Move item to next row", show=False, priority=True),
        Binding("P", "move_row('up')", "Move item to prev row", show=False, priority=True),
        Binding("r", "remove_selected", "Remove selected song from playlist", show=False)
    ]

    def action_remove_selected(self):
        key = self.find_key(self.cursor_row)
        if len(self.playlist) > 0 and key and self.parent:
            removed = self.playlist.pop(self.cursor_row)
            self.remove_row(key)
            available_table = self.parent.query_one(AvailableSongs)
            if len(self.data.songs[removed].name) > 97:
                 available_table.add_row(self.data.songs[removed].name[:94], key=str(removed))
            else:
                 available_table.add_row(self.data.songs[removed].name, key=str(removed))
            col_name = list(available_table.columns.keys())[0]
            available_table.sort(col_name, key=lambda x: x.lower())
            self.parent.check_change()


    def action_move_row(self, move: Literal["up", "down"]):
        new_row = None
        match (move):
            case "down":
                if self.cursor_row < self.row_count:
                    new_row = self.cursor_row + 1
            case "up":
                if self.cursor_row > 0:
                    new_row = self.cursor_row - 1

        if new_row is not None:
            value = self.playlist.pop(self.cursor_row)
            self.playlist.insert(new_row, value)
            self.sort(key=self.sort_key)
            self.cursor_coordinate = Coordinate(new_row, 0)
        if self.parent:
            self.parent.check_change()

    def sort_key(self, row : tuple[dt.RowKey, dict[dt.ColumnKey | str, dt.CellType]]):
        def len_check(id: int):
            if len(self.data.songs[id].name) > 97:
                return (self.data.songs[id].name[:94], id)
            return (self.data.songs[id].name, id)

        id_dict = dict(map(len_check, self.playlist))
        index_dict = dict(map(lambda x: (self.playlist[x], x), range(len(self.playlist))))
        return index_dict[id_dict[row[0]]]

class AvailableSongs(PlaylistTable):
    BINDINGS = [
        Binding("a", "add_selected", "Add to playlist", show=False),
    ]
    def __init__(self, *, data: Data, playlist: list[int], show_header: bool = True, show_row_labels: bool = True, fixed_rows: int = 0, fixed_columns: int = 0, zebra_stripes: bool = False, header_height: int = 1, show_cursor: bool = True, cursor_foreground_priority: Literal["renderable", "css"] = "css", cursor_background_priority: Literal["renderable", "css"] = "renderable", cursor_type: dt.CursorType = "cell", cell_padding: int = 1, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.playlist = playlist
        self.data = data
        super().__init__(show_header=show_header, show_row_labels=show_row_labels, fixed_rows=fixed_rows, fixed_columns=fixed_columns, zebra_stripes=zebra_stripes, header_height=header_height, show_cursor=show_cursor, cursor_foreground_priority=cursor_foreground_priority, cursor_background_priority=cursor_background_priority, cursor_type=cursor_type, cell_padding=cell_padding, name=name, id=id, classes=classes, disabled=disabled)

    def action_add_selected(self):
        def len_check(id: int):
            if len(self.data.songs[id].name) > 97:
                return (self.data.songs[id].name[:94], id)
            return (self.data.songs[id].name, id)
        id_dict = dict(map(len_check, self.data.songs))

        key = self.find_key(self.cursor_row)
        if key and self.parent:
            title = self.get_row(key)[0]

            added = id_dict[title]
            self.playlist.append(added)
            self.remove_row(key)

            playlist_table = self.parent.query_one(CurrentPlaylist)
            if len(self.data.songs[added].name) > 97:
                 playlist_table.add_row(self.data.songs[added].name[:94], key=str(added))
            else:
                 playlist_table.add_row(self.data.songs[added].name, key=str(added))
            self.parent.check_change()
