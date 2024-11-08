from ui.app import DNDSoundBoard
import os, pickle
from consts import DATA_PATH, MEDIA_PATH, FORMATS
from data import Data, Song

def main():
    if not os.path.exists(MEDIA_PATH):
        os.makedirs(MEDIA_PATH)

    # create file if does not exist
    if not os.path.exists(DATA_PATH):
        open(DATA_PATH, "wb").close()

    # dumps template if file is empty
    if not os.path.getsize(DATA_PATH) > 0:
        pickle.dump(Data(), open(DATA_PATH, 'wb'))

    old_data: Data = pickle.load(open(DATA_PATH, 'rb'))
    new_data = old_data.copy()

    media_files = []
    for f in os.listdir(MEDIA_PATH):
        if os.path.isfile(os.path.join(MEDIA_PATH, f)) and f.split(".")[-1] in FORMATS:
            media_files.append(f)
    media_files.sort(key=str.lower)

    file_saved = list(map(lambda x: x.file_name, old_data.songs))

    new_data.songs = list(filter(lambda x: x.file_name in media_files, old_data.songs))

    for i in range(len(media_files)):
        if media_files[i] not in file_saved:
            new_data.songs.append(Song(media_files[i]))

    new_data.songs.sort()

    pickle.dump(new_data, open(DATA_PATH, "wb+"))

    soundboard = DNDSoundBoard(new_data)
    soundboard.run()


main()
