# PyPlayer [![Latest Release](https://img.shields.io/github/release/thisismy-github/pyplayer/all.svg)](https://github.com/thisismy-github/pyplayer/releases) [![Download Count](https://img.shields.io/github/downloads/thisismy-github/pyplayer/total?color=success)](https://github.com/thisismy-github/pyplayer/releases/latest)

![Screenshot Gallery #1](https://i.imgur.com/NIebowT.png)

---

![Trimming](https://i.imgur.com/HBUnMDc.gif) ![Live cropping](https://i.imgur.com/5ew8Eua.gif)

## Editing features
- Concatenating/splicing
- Adding audio to images
- Fading
- Resizing (video dimensions and audio length/tempo)
- Rotating/flipping
- Audio amplification
- Track removal/replacement/addition
- And more! If you're reading from the future, that is.


## Other features
- Automatic updates
- Animated GIF support (experimental)
- Smooth zooming/panning (images/GIFs only for now)
- High-precision progress bar (experimental)
- Instantly cycle through media in the current folder
- Back/forward support for recent files
- Clicking on the player to pause
- Precise frame seeking
- Opening media in explorer and copying its path to your clipboard
- Renaming - Just type a new name in the text box at the bottom and press enter to instantly rename your file
- Deleting/recycling (recycled by default)
    - Mark files for later deletion (so you can change your mind), or instantly delete/recycle the file you have open
- Enhanced drag-and-drop
    - Drag media, folders, and subtitle files
    - Hold Ctrl/Shift/Alt while dropping to instantly concatenate files together or add audio tracks
- Snapshotting
    - Customize the size and aspect ratio of snapshots
    - Customize the naming format, image format, and quality (if applicable) of your snapshots
    - Use crop-mode to only snapshot the cropped region
    - Ability to view/explore/copy the most recent snapshot
    - Use snapshots to save cover art and extract GIF frames
- Ability to automatically resize window to match media's size and/or aspect ratio
    - This behavior can even be altered on-the-fly with Ctrl/Shift
- Pass arguments directly to the VLC instance as a string through the `-v`/`--vlc` argument


## Custom themes
PyPlayer supports custom themes in the form of Qt Stylesheets, which can come as .txt, .qss, or .css files. To add a custom theme, place it in the `themes` directory in the same directory as `pyplayer.exe`.

PyPlayer themes have minor differences from standard stylesheets and use their own "Theme" section. [View the included themes](https://github.com/thisismy-github/pyplayer/tree/master/themes) to get started with creating your own.


## Contributing
PyPlayer's code is meant to provide a more human-friendly implementation of VLC that can be easily built on and expanded, so contributions are very welcome. Translations, documentation (where necessary), tests, missing VLC features, themes, better cross-platform support, and new editing features are all especially welcome. If you're wondering where to start, there's well over one hundred TODOs dotted around the project, ranging from interesting to tedious to probably impossible. Most of these TODOs, ideas, and known issues are right at the top of [`main.pyw`](https://github.com/thisismy-github/pyplayer/blob/master/main.pyw).

Here are some basic guidelines:

- [If you're new to contributing in general, you can use this guide](https://www.dataschool.io/how-to-contribute-on-github/).
- Follow the [seven rules of a great commit message](https://cbea.ms/git-commit/#seven-rules).
- Try to match the style of the code surrounding your addition. Don't let your code stick out like a sore thumb.
- Try to keep your commits isolated to one general issue. Don't mash too many ideas into one commit, and avoid throwing in frivolous edits like changing the whitespace of random in-line comments (I do a LOT of frivolous edits in my own commits because I'm a hypocrite).
- Code should be as self-documenting as possible, with only minor explanatory comments/docstrings (if any).
- `bin/configparsebetter.py` is currently off-limits (part of a future project).
- Avoid changing the default themes unless it's to fix bugs or to add support for a new feature.
- Avoid introducing new, heavy dependencies where possible.
- Avoid relative paths where possible (use `constants.CWD` for the root folder).
- Be mindful of `constants.REPOSITORY_URL`. Make sure it points to the original repository when you make your commits, if you happen to change it while testing a feature.
