from ui.app import DNDSoundBoard
import os, pickle
from consts import DATA_PATH, MEDIA_PATH, FORMATS
from data import Data

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

    file_saved = list(map(lambda x: old_data.songs[x].file_name, old_data.songs))

    to_remove = list(filter(lambda file: file not in media_files, file_saved))
    to_add = list(filter(lambda file: file not in file_saved, media_files))
    for file in to_remove:
        new_data.remove_song(new_data.get_key("file_name", file))

    for file in to_add:
        new_data.add_song(file)

    if new_data != old_data:
        pickle.dump(new_data, open(DATA_PATH, "wb+"))

    soundboard = DNDSoundBoard(new_data)
    soundboard.run()


main()
