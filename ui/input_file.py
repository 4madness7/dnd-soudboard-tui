from textual.widgets import Input
from textual.events import Hide

class InputFile(Input):

    valid_empty = True

    def _on_hide(self, event: Hide) -> None:
        self.value = ""
        return super()._on_hide(event)

    def on_input_submitted(self):
        self.add_class("none")

