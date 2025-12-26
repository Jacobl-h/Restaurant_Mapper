#!/bin/bash

# Build script for Restaurant Mapper executable using PyInstaller

# Ensure PyInstaller is installed
pip install pyinstaller

# Clean previous builds
rm -rf build dist

# Build the executable
# --onefile: Bundles everything into a single executable
# --noconsole: Suppresses the console window (optional, but good for GUI apps).
#              However, keeping console might be useful for seeing the print statements if errors occur.
#              Given the user didn't explicitly ask to hide it, and the script prints progress,
#              I'll leave the console visible by default or maybe better to hide it since it's a GUI app.
#              "make it so that all you do is on a main popup" implies a GUI experience.
#              I will use --noconsole but users can remove it if they want debug info.
#              Wait, the print statements are useful. But for a polished app, console is usually hidden.
#              I'll add --noconsole but note it in comments.

pyinstaller --onefile --noconsole --name "RestaurantMapper" Restaurant_Mapper.py

echo "Build complete. Executable is in the 'dist' folder."
