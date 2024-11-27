import subprocess, os
from typing import Literal
from consts import MEDIA_PATH

class Data():
    def __init__(self, songs = {}, playlists = {}, soundboard = {}) -> None:
        self.songs = songs
        self.playlists = playlists
        self.soundboard = soundboard

    def __str__(self) -> str:
        return (
            "{\n" +
            f"\tSongs: {self.songs}\n" +
            f"\tPlaylists: {self.playlists}\n" +
            f"\tSoundboard: {self.soundboard}\n" +
            "}"
        )

    def __eq__(self, value) -> bool:
        return (
            self.songs == value.songs and
            self.playlists == value.playlists and
            self.soundboard == value.soundboard
        )

    def copy(self):
        return Data(
            self.songs.copy(),
            self.playlists.copy(),
            self.soundboard.copy()
        )

    def add_song(self, file_name: str) -> None:
        new_key = 0
        if len(self.songs) > 0:
            new_key = list(self.songs.keys())[-1] + 1
        self.songs.update({ new_key: Song(file_name=file_name) })

    def get_key(self, arg: Literal["name", "file_name"], key: str) -> int:
        match (arg):
            case "name":
                lst = dict(map(lambda kv: (kv[1].name, kv[0]), self.songs.items()))
            case "file_name":
                lst = dict(map(lambda kv: (kv[1].file_name, kv[0]), self.songs.items()))
        return lst[key]

    # TODO: you have to update this, remember you fooker
    def remove_song(self, key: int) -> None:
        self.songs.pop(key)


class Song():
    def __init__(self, name: str = "", file_name: str = "", duration: str = "XX:XX:XX") -> None:
        self.name = name
        if self.name == "":
            self.name = file_name.split(".")[0]
        self.file_name = file_name
        self.duration = duration
        self.calculate_audio_duration()

    def calculate_audio_duration(self) -> None:
        duration = "XX:XX:XX"
        res = subprocess.Popen(
            ["ffprobe",  "-i", os.path.join(MEDIA_PATH, self.file_name)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if res.stdout:
            duration = (res.communicate()[0]
                            .decode("utf8")
                            .split("Duration:")[1]
                            .split(".")[0]
                            .strip())
        self.duration = duration

    def copy(self):
        return Song(self.name, self.file_name, self.duration)

    def __str__(self) -> str:
        return (
            "{\n" +
            f"\tName: {self.name}\n" +
            f"\tFile name: {self.file_name}\n" +
            f"\tDuration: {self.duration}\n" +
            "}"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, value) -> bool:
        return self.name.lower() == value.name.lower()

    def __lt__(self, value):
        return self.name.lower() < value.name.lower()

    def __gt__(self, value):
        return self.name.lower() > value.name.lower()
