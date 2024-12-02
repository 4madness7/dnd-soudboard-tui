# dnd-soudboard-tui
Hello! This is my first personal project for [boot.dev](https://www.boot.dev).
It was a painful but rewarding project, I kinda like how it turned out, but I'm not really happy with the performance and with the overall experience while coding this project.
I think I'll rewrite this using GO sometime in the future.
I apologize for the errors in this file, English is not my first language so it's hard for me to explain things in English.
# What it does
This is a TUI wrapper around [python-mpv](https://pypi.org/project/python-mpv/) to create playlist and play in them background, with the addition of a soundboard to play sounds with the touch of a button.

This is meant to play background music while playing TTRPGS and have sound effects like footsteps, spell sounds, swords and so on.

# Installation and usage
## Using python venv
1. Clone the repo
```
git clone https://github.com/4madness7/dnd-soudboard-tui
```
2. Create a venv
```
python -m venv venv
```
3. Enter venv
```
source venv/bin/activate
```
4. Install requirements.txt
```
pip install -r requirementents.txt
```
5. Run main.py
```
python main.py
```
## Using shell.nix file
1. Clone the repo
```
git clone https://github.com/4madness7/dnd-soudboard-tui
```
2. Enter shell.nix file
```
nix-shell ./shell.nix
```
3. Run main.py
```
python main.py
```
