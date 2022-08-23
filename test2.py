import folium
# Create a map using Stamen Terrain, centered on Boulder, CO
m = folium.Map(location=[40.0150, -105.2705], 
               tiles = 'Stamen Terrain')

# Add marker for Boulder, CO
folium.Marker(
    location=[40.009515, -105.242714], # coordinates for the marker (Earth Lab at CU Boulder)
    popup='Earth Lab at CU Boulder', # pop-up label for the marker
    icon=folium.Icon()
).add_to(m)

# Display m
import WazeRouteCalculator
import logging

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
from_address = 'McDonalds Middle Island'
to_address = 'Chick Fil-A Port Jefferson NY'
region = 'US'
vehicle_type = 'CAR'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region, vehicle_type)
route.calc_route_info()
