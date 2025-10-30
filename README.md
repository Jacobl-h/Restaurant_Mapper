# Restaurant Mapper

An interactive data visualization tool built in Python that utilizes the Google Places API to search for restaurants of various cuisines within a specified radius of a given location and maps the results using the Folium library.
The resulting output is a single, filterable HTML file (restaurant_map.html) which allows users to:

View restaurants plotted as markers on an interactive map.

Filter restaurants based on a minimum star rating.

Toggle visibility of different cuisine layers.

# Features

Google Places API Integration: Uses googlemaps client for reliable geo-coding and nearby searches with built-in pagination handling to fetch maximum results.

Customizable Search: Users input a central street address and a custom search radius (in meters).

Interactive Mapping: Generates a stunning interactive map using Folium and Leaflet.js.

Dynamic Filtering: Includes a JavaScript slider on the map for real-time filtering of restaurants by minimum rating (e.g., show only restaurants rated 4.5 stars and above).

Cuisine Layer Control: Allows users to easily hide or show markers for specific cuisine categories.


# Prerequisites

Before you begin, you need to have Python and a few packages installed, and most importantly, a Google Cloud Project with the necessary APIs enabled.

1. Google API Key Setup (CRITICAL)

This script requires a valid Google API Key with the following services enabled in your Google Cloud Project:
Places API (for fetching nearby restaurant data).
Geocoding API (for converting the user-input street address to coordinates).

Steps to Obtain and Configure Your Key:
Go to the Google Cloud Console.
Create a new project (if you don't have one).
Navigate to APIs & Services > Credentials and generate an API key.
Important Security Step: Restrict the API key to prevent misuse. Configure it to only allow requests from the Places API and Geocoding API.
Open the Restaurant_Mapper_NOAPI.py file and replace the placeholder with your actual key:

# IMPORTANT: You must replace 'YOUR_API_KEY' with your actual API key
API_KEY = "YOUR_API_KEY"  # <-- Paste your key here!


# Installation
1. Clone the Repository
git clone [https://github.com/your-username/restaurant-mapper.git](https://github.com/your-username/restaurant-mapper.git)
cd restaurant-mapper


2. Python Environment Setup
It is highly recommended to use a virtual environment to manage dependencies.

Create a virtual environment
python3 -m venv venv

Activate the virtual environment

source venv/bin/activate  # On Linux/macOS
env\Scripts\activate  # On Windows


3. Install Required Libraries
Install the Python libraries specified in the script using pip:
pip install googlemaps folium pandas


The installed packages are:
googlemaps: For interfacing with the Google Places API.
folium: For generating the interactive Leaflet map.
pandas: Although not strictly necessary for the core functionality, it is often included in data projects, and your script imports it (though it doesn't use it, it's good practice to install all imported libraries).

# Usage
Once the API key is configured and dependencies are installed, you can run the script from your terminal:
python Restaurant_Mapper_NOAPI.py

The script will prompt you for two inputs:
Enter a street address to center the search on: (e.g., 123 Main St, New York, NY)
Enter a search radius in meters: (e.g., 5000 for 5 kilometers, or 50000 for 50 kilometers)

The script will then:
Geocode your address to latitude and longitude.
Iterate through the TOP_CUISINES list (defined in the Python file) and query the Google Places API for each.
Process and consolidate all the retrieved data.
Generate and save the interactive map file.

# Getting Results
Output File

After the script completes, a new file will be created in the same directory:

restaurant_map.html

Viewing the Map

Open this HTML file in any web browser to view the interactive map.
Markers: Each blue marker represents a restaurant. Click on a marker to see its name, rating, and number of reviews.
Rating Filter: Use the slider at the top of the map to dynamically hide markers that fall below the selected minimum star rating.
Cuisine Layers: Use the layer control box (usually on the top-right) to toggle the visibility of entire cuisine categories.

📁 File Structure
 .
 ├── Restaurant_Mapper_NOAPI.py  # The main Python script
 ├── README.md                  # This file
 └── venv/                      # Python virtual environment (after setup)
 └── restaurant_map.html        # GENERATED map output file


