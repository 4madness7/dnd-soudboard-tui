from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Static

class SoundEffects(ScrollableContainer):
    def compose(self) -> ComposeResult:
        for i in range(40):
            yield Static(f"{i}", classes="effect")
