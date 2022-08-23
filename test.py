import googlemaps
import geocoder
api_key = 'AIzaSyBXvNnlHVu4vp7CVQP8gA_loMG4GAJERks'
map_client = googlemaps.Client(api_key)
(lat, lng) = geocoder.ip('me').latlng[0], geocoder.ip('me').latlng[1]
curr_loc = (lat,lng)
response = map_client.distance_matrix(origins="28 Artist Drive Middle Island NY 11953", destinations="Chick Fil A Port Jefferson", mode="driving")
distance = response['rows'][0]['elements'][0]['distance']['text']
latlng1 = map_client.geocode(address="28 Artist Drive Middle Island NY 11953")[0]['geometry']['location']
latlng2 = map_client.geocode(address= "Chick Fil A Port Jefferson")[0]['geometry']['location']

p1 = latlng1['lat'], latlng1['lng']
p2 = latlng2['lat'], latlng2['lng']
print(map_client.nearest_roads(points=[p1,p2]))