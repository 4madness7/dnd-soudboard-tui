import pickle
import subprocess, os
from consts import MEDIA_PATH

class Data():
    def __init__(self, songs = [], playlists = {}, soundboard = []) -> None:
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

    def copy(self):
        return Data(self.songs, self.playlists, self.soundboard)

    def add_song(self, file_name: str) -> None:
        self.songs.append(Song(file_name))
        self.songs.sort()


class Song():
    def __init__(self, file_name: str = "") -> None:
        self.name = file_name.split(".")[0]
        self.file_name = file_name
        self.duration = "XX:XX:XX"
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

    def __str__(self) -> str:
        return (
            "\n{\n" +
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
