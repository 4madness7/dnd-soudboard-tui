from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Static, Collapsible

class Playlists(ScrollableContainer):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Playlist", collapsed=False):
            yield Static("1. Song 1")
            yield Static("2. Song 2")
            yield Static("3. Song 3")
            yield Static("4. Song 4")
            yield Static("5. Song 5")
            yield Static("6. Song 6")
            yield Static("7. Song 7")
            yield Static("8. Song 8")
            yield Static("9. Song 9")
        with Collapsible(title="Playlist", collapsed=False):
            yield Static("1. Song 1")
            yield Static("2. Song 2")
            yield Static("3. Song 3")
            yield Static("4. Song 4")
            yield Static("5. Song 5")
            yield Static("6. Song 6")
            yield Static("7. Song 7")
            yield Static("8. Song 8")
            yield Static("9. Song 9")
        with Collapsible(title="Playlist", collapsed=False):
            yield Static("1. Song 1")
            yield Static("2. Song 2")
            yield Static("3. Song 3")
            yield Static("4. Song 4")
            yield Static("5. Song 5")
            yield Static("6. Song 6")
            yield Static("7. Song 7")
            yield Static("8. Song 8")
            yield Static("9. Song 9")
        with Collapsible(title="Playlist", collapsed=False):
            yield Static("1. Song 1")
            yield Static("2. Song 2")
            yield Static("3. Song 3")
            yield Static("4. Song 4")
            yield Static("5. Song 5")
            yield Static("6. Song 6")
            yield Static("7. Song 7")
            yield Static("8. Song 8")
            yield Static("9. Song 9")
