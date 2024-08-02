import networkx as nx
import folium
from geopy.geocoders import Nominatim

# Initialize geolocator
geolocator = Nominatim(user_agent="city_map")

def get_location(address):
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)

# Example addresses
addresses = ["Times Square, New York, NY", "Central Park, New York, NY", "Empire State Building, New York, NY"]
locations = {address: get_location(address) for address in addresses}

# Create a graph
G = nx.Graph()

# Add nodes
for address, coords in locations.items():
    G.add_node(address, pos=coords)

# Add edges (example edges with hypothetical distances)
edges = [
    ("Times Square, New York, NY", "Central Park, New York, NY", 1.5),
    ("Times Square, New York, NY", "Empire State Building, New York, NY", 1.0),
    ("Central Park, New York, NY", "Empire State Building, New York, NY", 2.0)
]
G.add_weighted_edges_from(edges)

# Apply Dijkstra's Algorithm
start_address = "Times Square, New York, NY"
end_address = "Empire State Building, New York, NY"
shortest_path = nx.dijkstra_path(G, start_address, end_address, weight='weight')
print(f"Shortest path: {shortest_path}")

# Create a folium map centered around the first location
m = folium.Map(location=locations[start_address], zoom_start=14)

# Add nodes to the map
for address, coords in locations.items():
    folium.Marker(location=coords, popup=address).add_to(m)

# Add edges to the map
for start, end, _ in edges:
    folium.PolyLine(locations=[locations[start], locations[end]], color='blue').add_to(m)

# Highlight the shortest path
path_coords = [locations[address] for address in shortest_path]
folium.PolyLine(locations=path_coords, color='red', weight=5).add_to(m)

# Save the map to an HTML file
m.save('city_map.html')
