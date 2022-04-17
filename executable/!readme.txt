---

To compile PyPlayer on Windows, simply run "build.py".

This assumes that you have pip and already have all the appropriate libraries from
requirements.txt installed. If not, you can do "pip -r --upgrade requirements.txt".

For compatibility with Windows 7 and Windows Vista, Python 3.8 must be used.

---

Summary of contents:
    include           -- These are the excess files that are needed by PyPlayer, which currently
                         includes the two required libvlc .dlls, and all of the currently used VLC
                         plugins. If users already have these files in their PATH, (i.e. ffmpeg and
                         VLC are installed) then they do not actually need to be included.

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

    build.py          -- A cross-platform Python script for compiling. This searches for a venv, uses
                         the .spec files to compile both PyPlayer and its updater, and then performs
                         several post-compilation activities to clean up and finish the compile.

    exclude.txt       -- This contains a list of likely files and folders to be included with each
                         compilation on Windows that do not appear to actually be necessary and
                         will be deleted automatically after compilation. Based on compilations
                         done through a virtualenv on Windows 10 and Windows 7, using only the
                         packages in requirements.txt.

    hook.py           -- A runtime hook added to main.spec which runs at startup, decides whether to
                         open a new PyPlayer instance or reuse an existing one, adds the PyQt5 folder
                         to sys.path (allowing the executable to look for .dll and .pyd files inside
                         the PyQt5 folder, which must exist regardless, letting us hide many files
                         and cut down on clutter), and sets the location of necessary VLC files.

    *.spec            -- PyInstaller .spec files specifying how to compile PyPlayer's two main
                         scripts, main.pyw and updater.pyw.
