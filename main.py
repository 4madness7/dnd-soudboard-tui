from ui.app import DNDSoundBoard
import os

MEDIA_PATH = os.path.join(os.getcwd(), "media")

def main():
    if not os.path.exists(MEDIA_PATH):
        os.makedirs(MEDIA_PATH)

    soundboard = DNDSoundBoard()
    soundboard.run()


main()
