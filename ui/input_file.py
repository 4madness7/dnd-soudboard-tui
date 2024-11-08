import pickle
from textual.widgets import Input
from textual.events import Hide
import os

from consts import DATA_PATH, FORMATS
from data import Data
from utils import copy_file

class InputFile(Input):
    def __init__(self, data: Data,  placeholder: str = "", classes: str | None = None) -> None:
        self.data = data
        super().__init__(None, placeholder, None, False, classes=classes)

    valid_empty = True

    def _on_hide(self, event: Hide) -> None:
        self.value = ""
        return super()._on_hide(event)

    def on_input_submitted(self):
        input_path = self.value.strip()
        self.add_class("none")

        is_file = os.path.isfile(input_path)
        is_dir = os.path.isdir(input_path)
        is_audio_file = input_path.split(".")[-1] in FORMATS
        if is_dir:
            media_files = []
            for f in os.listdir(input_path):
                if os.path.isfile(os.path.join(input_path, f)) and f.split(".")[-1] in FORMATS:
                    media_files.append(f)
            media_files.sort()

            count_saved = 0
            for file_name in media_files:
                copied, new_path = copy_file(os.path.join(input_path, file_name))
                if copied:
                    self.data.add_song(file_name)
                    count_saved += 1
                else:
                    self.app.notify(f"File \"{new_path}\" already exists", severity="error")

            if count_saved > 0:
                pickle.dump(self.data, open(DATA_PATH, "wb+"))

            self.app.notify(
                f"Successfully copied {count_saved} audio files out of {len(media_files)}.",
                severity="information"
            )
        elif is_file and is_audio_file:
            copied, new_path = copy_file(input_path)
            if copied:
                self.data.add_song(new_path.split(os.sep)[-1])
                pickle.dump(self.data, open(DATA_PATH, "wb+"))

                self.app.notify(
                    f"Successfully copied audio from \"{input_path}\" to \"{new_path}\"",
                    severity="information"
                )
            else:
                self.app.notify(f"File \"{new_path}\" already exists", severity="error")
        else:
            if not is_dir:
                self.app.notify("Directory not found", severity="error")
            if not is_file:
                self.app.notify("File not found", severity="error")
            elif not is_audio_file:
                self.app.notify(f"Not a valid format. Valid formats: {FORMATS}", severity="error")

