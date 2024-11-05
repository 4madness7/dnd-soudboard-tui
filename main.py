from ui.app import DNDSoundBoard
import os
from consts import MEDIA_PATH

def main():
    if not os.path.exists(MEDIA_PATH):
        os.makedirs(MEDIA_PATH)

    soundboard = DNDSoundBoard()
    soundboard.run()


main()
