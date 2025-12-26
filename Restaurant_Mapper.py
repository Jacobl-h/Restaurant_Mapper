# This script fetches restaurant data using the Google Places API
# and then generates an interactive HTML map using the Folium library.

import googlemaps
import json
import time
import folium
import os
import webbrowser
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from folium import IFrame, plugins

API_KEY_FILE = "api_key.txt"
CUISINES_FILE = "cuisines.txt"

def get_restaurants_by_cuisine(client, cuisine, location, radius):
    """
    Searches for restaurants of a specific cuisine and handles pagination.
    """
    print(f"Searching for {cuisine} restaurants...")
    all_results = []

    try:
        # We've changed this to 'client.places_nearby' which is the correct
        # function for a "nearby search" that uses location and radius,
        # and it properly accepts the 'keyword' parameter.
        places_result = client.places_nearby(
            location=location,
            radius=radius,
            type="restaurant",  # The 'type' parameter is required for 'places_nearby'
            keyword=cuisine
        )

        if 'results' in places_result:
            all_results.extend(places_result['results'])

        # Pagination loop to get more results
        next_page_token = places_result.get('next_page_token')
        while next_page_token:
            # Pause to avoid "OVER_QUERY_LIMIT"
            time.sleep(2)

            # For subsequent pages, we only need the token.
            places_result = client.places_nearby(
                page_token=next_page_token
            )

            if 'results' in places_result:
                all_results.extend(places_result['results'])

            next_page_token = places_result.get('next_page_token')

    except Exception as e:
        print(f"An error occurred: {e}")

    return all_results

def geocode_address(client, address):
    """
    Converts a street address into latitude and longitude coordinates.
    """
    try:
        geocode_result = client.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            print("Could not find coordinates for the provided address.")
            return None
    except Exception as e:
        print(f"Error geocoding address: {e}")
        return None

def generate_map(restaurants_data, filename="restaurant_map.html"):
    """
    Generates an interactive map with markers and a rating filter.
    The map is saved as a single HTML file.
    """
    # Create a base map centered on the first restaurant found, or LA
    la_location = (34.0522, -118.2437)

    # If there is data, center the map on the first restaurant to provide a better initial view.
    if restaurants_data:
        first_restaurant_location = (restaurants_data[0]['lat'], restaurants_data[0]['lng'])
        base_map = folium.Map(location=first_restaurant_location, zoom_start=13)
    else:
        base_map = folium.Map(location=la_location, zoom_start=10)

    # Process restaurant data to be ready for JSON.
    js_data = restaurants_data

    # This is the more reliable way to inject JavaScript into the HTML.
    # We create a new script element and add it to the body of the map.
    js_code = """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var all_restaurants = """ + json.dumps(js_data) + """;
                var cuisineLayers = {};
                var mapInstance = """ + base_map.get_name() + """;

                // Set z-index for Leaflet controls to ensure they are on top.
                var mapPane = document.querySelector('.leaflet-control-container');
                if (mapPane) {
                    mapPane.style.zIndex = 1000;
                }

                // Cuisine layer control
                var layerControlDiv = L.DomUtil.create('div', 'leaflet-control-layers leaflet-control');
                layerControlDiv.style.position = 'absolute';
                layerControlDiv.style.top = '10px';
                layerControlDiv.style.right = '10px';
                layerControlDiv.style.zIndex = 1001; // Ensure this is above other map elements
                mapInstance.getContainer().appendChild(layerControlDiv);

                var cuisines = [...new Set(all_restaurants.map(r => r.cuisine))];
                cuisines.forEach(function(cuisine) {
                    cuisineLayers[cuisine] = L.layerGroup();
                });

                var layerControl = L.control.layers({}, cuisineLayers, {collapsed: false}).addTo(mapInstance);

                // We've changed the position to be more reliable and visible.
                var sliderDiv = L.DomUtil.create('div', 'leaflet-control');
                sliderDiv.style.position = 'absolute';
                sliderDiv.style.top = '10px';
                sliderDiv.style.left = '50%';
                sliderDiv.style.transform = 'translateX(-50%)';
                sliderDiv.style.background = 'white';
                sliderDiv.style.padding = '15px';
                sliderDiv.style.borderRadius = '10px';
                sliderDiv.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
                sliderDiv.style.display = 'flex';
                sliderDiv.style.alignItems = 'center';
                sliderDiv.style.gap = '10px';
                sliderDiv.style.zIndex = 1001; // Ensure this is above other map elements

                sliderDiv.innerHTML = `
                    <label for="rating-slider" style="font-family: sans-serif; font-size: 14px; white-space: nowrap;">Min. Rating: </label>
                    <input type="range" id="rating-slider" min="1" max="5" value="4" step="0.1" style="width: 200px;">
                    <span id="rating-value" style="font-family: monospace; font-size: 14px; font-weight: bold; width: 40px; text-align: right;">4.0</span>
                `;

                mapInstance.getContainer().appendChild(sliderDiv);

                var slider = document.getElementById('rating-slider');
                var valueSpan = document.getElementById('rating-value');

                function updateMapMarkers() {
                    var minRating = parseFloat(slider.value);
                    valueSpan.textContent = minRating.toFixed(1);

                    // Clear all existing markers
                    Object.values(cuisineLayers).forEach(layer => layer.clearLayers());

                    // Add markers for each cuisine based on the filter
                    cuisines.forEach(function(cuisine) {
                        all_restaurants.filter(r => r.cuisine === cuisine).forEach(function(r) {
                            if (r.rating >= minRating) {
                                var popupContent = '<b>' + r.name + '</b><br>Rating: ' + r.rating + ' stars<br>Reviews: ' + r.reviews;
                                var marker = L.circleMarker([r.lat, r.lng], {
                                    radius: 5,
                                    color: '#007bff', // Use a nice blue color
                                    fillColor: '#007bff',
                                    fillOpacity: 0.7
                                }).bindPopup(popupContent);
                                marker.addTo(cuisineLayers[cuisine]);
                            }
                        });
                    });
                }

                updateMapMarkers();
                slider.addEventListener('input', updateMapMarkers);

                // Add all layers initially
                cuisines.forEach(function(cuisine) {
                    cuisineLayers[cuisine].addTo(mapInstance);
                });
            });
        </script>
    """

    # Add the JavaScript code to the map's root HTML.
    base_map.get_root().html.add_child(folium.Element(js_code))

    # Save the map as a standalone HTML file
    if not filename.endswith('.html'):
        filename += '.html'

    base_map.save(filename)
    print(f"Interactive map successfully generated and saved to {filename}")
    return os.path.abspath(filename)

def run_mapper(api_key, address, radius, cuisines_list, map_name):
    """
    Main execution logic, to be called by the GUI.
    """
    # Initialize the Google Maps client
    try:
        gmaps = googlemaps.Client(key=api_key)
    except Exception as e:
        print(f"Error initializing Google Maps client. Make sure your API key is correct. Error: {e}")
        raise ValueError(f"Invalid API Key or connection error: {e}")

    # Geocode the user-provided address
    location_coords = geocode_address(gmaps, address)
    if not location_coords:
        # If geocoding fails, we can't really proceed effectively with a "nearby" search centered on nothing.
        # But per original logic, it fell back to LA. We'll stick to that or raise error.
        # Let's raise error to inform user.
        raise ValueError("Could not find coordinates for the provided address.")

    all_data = []

    # Fetch data for each cuisine
    for cuisine in cuisines_list:
        if not cuisine.strip():
            continue

        try:
            restaurants = get_restaurants_by_cuisine(gmaps, cuisine.strip(), location_coords, radius)

            # Use a temporary list to safely process and append new data
            clean_data = []
            for r in restaurants:
                # Add robust checks to ensure a restaurant has all the necessary fields
                if all(key in r and r[key] is not None for key in ['geometry', 'name', 'rating']) and 'location' in r['geometry']:

                    # Also check for valid latitude and longitude values
                    lat = r['geometry']['location'].get('lat')
                    lng = r['geometry']['location'].get('lng')

                    if lat is not None and lng is not None:
                        clean_data.append({
                            'name': r.get('name', 'N/A'),
                            'lat': lat,
                            'lng': lng,
                            'rating': r.get('rating', 0),
                            'reviews': r.get('user_ratings_total', 0),
                            'cuisine': cuisine.strip()
                        })

            all_data.extend(clean_data)

            # Inform the user about the number of restaurants found for this cuisine
            print(f"Found {len(clean_data)} {cuisine} restaurants.")
        except Exception as e:
            # If the API call fails, we continue to the next cuisine
            print(f"Failed to retrieve data for {cuisine}: {e}")

    # Generate and save the interactive map
    return generate_map(all_data, map_name)

class RestaurantMapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Mapper")
        self.root.geometry("500x600")

        # Load saved data
        self.saved_api_key = self.load_file(API_KEY_FILE)
        self.saved_cuisines = self.load_file(CUISINES_FILE)

        self.create_widgets()

    def load_file(self, filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return f.read().strip()
            except Exception:
                return ""
        return ""

    def save_file(self, filepath, content):
        try:
            with open(filepath, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Error saving {filepath}: {e}")

    def create_widgets(self):
        # API Key
        tk.Label(self.root, text="Google API Key:").pack(pady=(10, 0))
        self.api_key_entry = tk.Entry(self.root, width=50)
        self.api_key_entry.insert(0, self.saved_api_key)
        self.api_key_entry.pack(pady=5)

        # Address
        tk.Label(self.root, text="Address (Center of Search):").pack(pady=(10, 0))
        self.address_entry = tk.Entry(self.root, width=50)
        self.address_entry.pack(pady=5)

        # Radius
        tk.Label(self.root, text="Radius (meters):").pack(pady=(10, 0))
        self.radius_entry = tk.Entry(self.root, width=50)
        self.radius_entry.insert(0, "5000")
        self.radius_entry.pack(pady=5)

        # Map Name
        tk.Label(self.root, text="Map Name:").pack(pady=(10, 0))
        self.map_name_entry = tk.Entry(self.root, width=50)
        self.map_name_entry.insert(0, "MyRestaurantMap")
        self.map_name_entry.pack(pady=5)

        # Cuisines
        tk.Label(self.root, text="Cuisines (comma separated or new line):").pack(pady=(10, 0))
        self.cuisines_text = scrolledtext.ScrolledText(self.root, height=10, width=50)
        self.cuisines_text.insert("1.0", self.saved_cuisines)
        self.cuisines_text.pack(pady=5)

        # Run Button
        self.run_btn = tk.Button(self.root, text="Generate Map", command=self.on_run, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.run_btn.pack(pady=20)

    def on_run(self):
        api_key = self.api_key_entry.get().strip()
        address = self.address_entry.get().strip()
        radius_str = self.radius_entry.get().strip()
        map_name = self.map_name_entry.get().strip()
        cuisines_raw = self.cuisines_text.get("1.0", tk.END).strip()

        # Validation
        if not api_key:
            messagebox.showerror("Error", "Please enter an API Key.")
            return
        if not address:
            messagebox.showerror("Error", "Please enter an address.")
            return
        if not radius_str.isdigit():
            messagebox.showerror("Error", "Radius must be a number.")
            return
        if not cuisines_raw:
            messagebox.showerror("Error", "Please enter at least one cuisine.")
            return

        radius = int(radius_str)
        cuisines_list = [c.strip() for c in cuisines_raw.replace('\n', ',').split(',') if c.strip()]

        # Save persistence data
        self.save_file(API_KEY_FILE, api_key)
        self.save_file(CUISINES_FILE, cuisines_raw)

        # Disable button while processing
        self.run_btn.config(state=tk.DISABLED, text="Processing...")

        # Run in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.run_process_thread, args=(api_key, address, radius, cuisines_list, map_name))
        thread.start()

    def run_process_thread(self, api_key, address, radius, cuisines_list, map_name):
        try:
            output_path = run_mapper(api_key, address, radius, cuisines_list, map_name)
            # Schedule UI update on main thread
            self.root.after(0, lambda: self.on_success(output_path))
        except Exception as e:
            # Schedule UI update on main thread
            self.root.after(0, lambda: self.on_error(str(e)))

    def on_success(self, output_path):
        webbrowser.open('file://' + output_path)
        folder_dir = os.path.dirname(output_path)
        messagebox.showinfo("Success", f"Your map has been saved as {os.path.basename(output_path)} in {folder_dir}")
        self.run_btn.config(state=tk.NORMAL, text="Generate Map")

    def on_error(self, error_msg):
        messagebox.showerror("Error", f"An error occurred: {error_msg}")
        self.run_btn.config(state=tk.NORMAL, text="Generate Map")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantMapperApp(root)
    root.mainloop()
