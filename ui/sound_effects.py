from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button
from textual.binding import Binding
from textual.events import Focus
from typing import Literal

class SoundEffects(ScrollableContainer):
    BINDINGS = [
        Binding("down,j", "move_focus('down')", "Focus sound under selected", show=False),
        Binding("up,k", "move_focus('up')", "Focus sound up selected", show=False),
        Binding("left,h", "move_focus('left')", "Focus sound to the left of selected", show=False),
        Binding("right,l", "move_focus('right')", "Focus sound to the right of selected", show=False),
    ]

    focused_child = 0

    def compose(self) -> ComposeResult:
        for i in range(40):
            yield Button(f"{i}", classes="effect")

    def action_move_focus(self, direction: Literal["up", "down", "left", "right"]) -> None:
        state = self.query(Button)
        i = 0
        while not state.nodes[i].has_focus:
            if i >= len(state.nodes) - 1:
                break
            i += 1
        match (direction):
            case 'down':
                self.focused_child = (i + 2) % len(state.nodes)
            case 'up':
                self.focused_child = (i - 2) % len(state.nodes)
            case 'right':
                self.focused_child = (i + 1) % len(state.nodes)
            case 'left':
                self.focused_child = (i - 1) % len(state.nodes)
        state.nodes[self.focused_child].focus()


    def _on_focus(self, event: Focus) -> None:
        self.children[self.focused_child].focus()
        return super()._on_focus(event)
