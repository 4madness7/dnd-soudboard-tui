from textual.widgets import Input
from textual.events import Hide
import os
import shutil

from consts import FORMATS, MEDIA_PATH

class InputFile(Input):

    valid_empty = True

    def _on_hide(self, event: Hide) -> None:
        self.value = ""
        return super()._on_hide(event)

    def on_input_submitted(self):
        self.value = self.value.strip()
        is_file = os.path.isfile(self.value)
        is_audio_file = self.value.split(".")[-1] in FORMATS
        if is_file and is_audio_file:
            filename = os.path.split(self.value)[-1]
            full_path = os.path.join(MEDIA_PATH, filename)
            if not os.path.exists(full_path):
                shutil.copyfile(self.value, full_path,follow_symlinks=False)
                self.app.notify(
                        f"Successfully copied audio from \"{self.value}\" to \"{full_path}\"",
                        severity="information"
                    )
            else:
                self.app.notify(f"File \"{full_path}\" already exists", severity="error")
        else:
            if not is_file:
                self.app.notify("File not found", severity="error")
            if not is_audio_file:
                self.app.notify(f"Not a valid format. Valid formats: {FORMATS}", severity="error")
        self.add_class("none")

