---

To compile PyPlayer on Windows, simply run "build-windows.bat" in the main folder.

This assumes that you have pip and already have all the appropriate libraries from
requirements.txt installed. If not, you can do "pip -r --upgrade requirements.txt".

---

Summary of contents:
    include           -- These are the excess files that are needed by PyPlayer, including libvlc
                         .dlls, VLC's plugins folder, and a small copy of ffmpeg. If users already
                         have all of these files accessible through their PATH, then they do not
                         actually need to be included with the executable.

    build             -- PyInstaller build files that are created during the first compilation.
                         These are not needed for anything, but speed up future compilations.

    compiled          -- PyInstaller's actual compilation folder. This is where the final products
                         are placed. Normally called "dist", but renamed to "compiled" for clarity.

    compiled/release  -- The compiled files for PyPlayer's main script, main.pyw. This is where
                         compiled files for the launcher and updater will be merged, the "include"
                         files may be added, and all of PyPlayer's other misc files will be placed.
                         If using build-windows.bat, the launcher and updater folders will be merged
                         and deleted automatically, and all misc/include files will be merged as well.
                         As the name implies, this is the folder that would be released on Github.

    *.spec            -- PyInstaller .spec files specifying how to compile PyPlayer's three
                         main scripts, main.pyw, launcher.pyw, and updater.pyw.
