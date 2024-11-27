from typing import Literal
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import data_table as dt, DataTable, Label
from textual.binding import Binding
from textual.events import Focus
import pickle
from ui.edit_playlist import PlaylistTable

from consts import DATA_PATH
from data import Data

COL_MAX_CHARS = 92
STR_MAX_CHARS = COL_MAX_CHARS - 3

class EditSoundBoard(Vertical):
    BINDINGS = [
        Binding("j", "move_focus('down')", "Move down to next table", show=False),
        Binding("k", "move_focus('up')", "Move up to next table", show=False),
        Binding("S", "save", "Save changes", show=False)
    ]

    def __init__(self, data: Data,*children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.data = data
        self.soundboard: dict[int, str] = {}
        self.focused_child = 0
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)

    can_focus = True

    def compose(self) -> ComposeResult:
        self.soundboard = self.data.soundboard.copy()

        yield Horizontal(
            Label(f"CurrentPlaylist: [b]Sound effects[/b] |"),
            SaveStatus(),
            classes="w-100"
        )

        table = CurrentSoundboard(cursor_type="none", data=self.data ,playlist=self.soundboard)
        table.add_columns("Key", "Sound name".ljust(COL_MAX_CHARS))
        for id in self.soundboard:
            if len(self.data.songs[id].name) > COL_MAX_CHARS:
                table.add_row("N/A", self.data.songs[id].name[:STR_MAX_CHARS], key=str(id))
            else:
                table.add_row("N/A", self.data.songs[id].name, key=str(id))
        yield table

        yield Label("Available Songs")
        remaining_songs = list(set(self.data.songs.keys()) - set(self.soundboard.keys()))
        table = AvailableSounds(cursor_type="none", data=self.data, soundboard=self.soundboard)
        _, col_key_name = table.add_columns("Key", "Sound name".ljust(COL_MAX_CHARS))
        for id in remaining_songs:
            if len(self.data.songs[id].name) > COL_MAX_CHARS:
                table.add_row("N/A", self.data.songs[id].name[:STR_MAX_CHARS], key=str(id))
            else:
                table.add_row("N/A", self.data.songs[id].name, key=str(id))
        table.sort(col_key_name, key=lambda name: name.lower())
        yield table

    def check_change(self):
        self.query_one(SaveStatus).changes = self.data.soundboard != self.soundboard

    def refresh_playlist_table(self):
        sound_effects = self.app.query_one("SoundEffects")
        sound_effects.update_table()

    def action_save(self):
        status = self.query_one(SaveStatus)
        if status.changes:
            self.data.soundboard = self.soundboard.copy()
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
        if self.changes:
            self.add_class("save-warning")
            return "There are unsaved changes."
        self.remove_class("save-warning")
        return "Saved."

class CurrentSoundboard(PlaylistTable):
    def __init__(self, *, data: Data, playlist, show_header: bool = True, show_row_labels: bool = True, fixed_rows: int = 0, fixed_columns: int = 0, zebra_stripes: bool = False, header_height: int = 1, show_cursor: bool = True, cursor_foreground_priority: Literal["renderable", "css"] = "css", cursor_background_priority: Literal["renderable", "css"] = "renderable", cursor_type: dt.CursorType = "cell", cell_padding: int = 1, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.soundboard: dict[int, str] =  playlist
        self.data = data
        super().__init__(show_header=show_header, show_row_labels=show_row_labels, fixed_rows=fixed_rows, fixed_columns=fixed_columns, zebra_stripes=zebra_stripes, header_height=header_height, show_cursor=show_cursor, cursor_foreground_priority=cursor_foreground_priority, cursor_background_priority=cursor_background_priority, cursor_type=cursor_type, cell_padding=cell_padding, name=name, id=id, classes=classes, disabled=disabled)

    BINDINGS = [
        Binding("r", "remove_selected", "Remove selected song from playlist", show=False)
    ]

    def action_remove_selected(self):
        key = self.find_key(self.cursor_row)
        if len(self.soundboard) > 0 and key and key.value and self.parent:
            removed = int(key.value)
            self.soundboard.pop(removed)
            self.remove_row(key)
            available_table = self.parent.query_one(AvailableSounds)
            if len(self.data.songs[removed].name) > COL_MAX_CHARS:
                 available_table.add_row("N/A", self.data.songs[removed].name[:STR_MAX_CHARS], key=str(removed))
            else:
                 available_table.add_row("N/A", self.data.songs[removed].name, key=str(removed))
            col_name = list(available_table.columns.keys())[1]
            available_table.sort(col_name, key=lambda x: x.lower())
            self.parent.check_change()

class AvailableSounds(PlaylistTable):
    BINDINGS = [
        Binding("a", "add_selected", "Add to playlist", show=False),
    ]

    def __init__(self, *, data: Data, soundboard: dict[int, str], show_header: bool = True, show_row_labels: bool = True, fixed_rows: int = 0, fixed_columns: int = 0, zebra_stripes: bool = False, header_height: int = 1, show_cursor: bool = True, cursor_foreground_priority: Literal["renderable", "css"] = "css", cursor_background_priority: Literal["renderable", "css"] = "renderable", cursor_type: dt.CursorType = "cell", cell_padding: int = 1, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        self.soundboard = soundboard
        self.data = data
        super().__init__(show_header=show_header, show_row_labels=show_row_labels, fixed_rows=fixed_rows, fixed_columns=fixed_columns, zebra_stripes=zebra_stripes, header_height=header_height, show_cursor=show_cursor, cursor_foreground_priority=cursor_foreground_priority, cursor_background_priority=cursor_background_priority, cursor_type=cursor_type, cell_padding=cell_padding, name=name, id=id, classes=classes, disabled=disabled)

    def action_add_selected(self):
        def len_check(id: int):
            if len(self.data.songs[id].name) > COL_MAX_CHARS:
                return (self.data.songs[id].name[:STR_MAX_CHARS], id)
            return (self.data.songs[id].name, id)
        id_dict = dict(map(len_check, self.data.songs))

        key = self.find_key(self.cursor_row)
        if key and self.parent:
            title = self.get_row(key)[1]

            added = id_dict[title]
            self.soundboard[added] = "N/A"
            self.remove_row(key)

            playlist_table = self.parent.query_one(CurrentSoundboard)
            if len(self.data.songs[added].name) > COL_MAX_CHARS:
                 playlist_table.add_row(self.soundboard[added], self.data.songs[added].name[:STR_MAX_CHARS], key=str(added))
            else:
                 playlist_table.add_row(self.soundboard[added], self.data.songs[added].name, key=str(added))
            col_name = list(playlist_table.columns.keys())[1]
            playlist_table.sort(col_name, key=lambda x: x.lower())
            self.parent.check_change()
