# Restaurant Mapper

An interactive data visualization tool built in Python that utilizes the Google Places API to search for restaurants of various cuisines within a specified radius of a given location and maps the results using the Folium library.

**Now with a Graphical User Interface (GUI) and executable support!**

## Features

*   **GUI Interface:** Easy-to-use popup window to enter all settings.
*   **Persistence:** Automatically remembers your API Key and Cuisines list between sessions.
*   **Custom Map Naming:** Name your output map file.
*   **Automatic Display:** The generated map opens automatically in your web browser.
*   **Google Places API Integration:** Uses googlemaps client for reliable geo-coding and nearby searches.
*   **Interactive Mapping:** Generates a stunning interactive map using Folium.

## Prerequisites

1.  **Google API Key (CRITICAL)**
    *   This app requires a valid Google API Key with **Places API** and **Geocoding API** enabled.
    *   [Get an API Key here](https://developers.google.com/maps/documentation/places/web-service/get-api-key).

## Usage

### Running from Source

1.  **Install Python:** Ensure Python 3.x is installed.
2.  **Install Dependencies:**
    ```bash
    pip install googlemaps folium pandas
    ```
    *(Note: `pandas` is not strictly used but included in requirements)*
3.  **Run the App:**
    ```bash
    python Restaurant_Mapper.py
    ```
4.  **Fill in the details:**
    *   **API Key:** Paste your Google API Key.
    *   **Address:** Enter the center point for your search (e.g., "New York, NY").
    *   **Radius:** Search radius in meters.
    *   **Map Name:** Name for the output file (e.g., "FridayNightDinner").
    *   **Cuisines:** List the cuisines you want to search for. You can separate them by commas or new lines.
5.  **Click "Generate Map"**: The app will fetch data and open the map in your browser.

### Building the Executable (.exe)

To create a standalone `.exe` file that runs without installing Python manually:

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Build:**
    Run the included build script:
    ```bash
    ./build_exe.sh
    ```
    Or run the command manually:
    ```bash
    pyinstaller --onefile --noconsole --name "RestaurantMapper" Restaurant_Mapper.py
    ```
3.  **Locate the Exe:**
    The generated executable will be in the `dist` folder. You can move this `RestaurantMapper.exe` anywhere on your computer.
    *   *Note:* The `api_key.txt` and `cuisines.txt` files will be created in the same folder where the `.exe` is located after the first run.

## File Structure

*   `Restaurant_Mapper.py`: The main application script.
*   `build_exe.sh`: Script to build the executable.
*   `README.md`: This file.
*   `dist/`: Folder containing the compiled executable (after building).

