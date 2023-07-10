import haversine as hs
from haversine import Unit
from geopy.geocoders import Nominatim
import WazeRouteCalculator
import logging

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
from_address = '28 Artist Drive Middle Island'
to_address = 'Chick Fil-A Port Jefferson NY'
region = 'US'
vehicle_type = 'CAR'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region, vehicle_type)
route.calc_route_info()


# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

def parseCoords(loc):
    coordslat = geolocator.geocode(loc).latitude
    coordslng = geolocator.geocode(loc).longitude
    coords = coordslat, coordslng
    return coords 

def obtainMileage(deliveries):
    currLoc = geolocator.geocode("28 Artist Drive Middle Island").latitude, geolocator.geocode("28 Artist Drive Middle Island").longitude
    for (pickup, dest) in deliveries:
        pickupCoords = parseCoords(pickup)
        destCoords = parseCoords(dest)
        deliveryMileage = hs.haversine(pickupCoords,destCoords,unit=Unit.MILES)
        fromStartMileage = hs.haversine(currLoc,pickupCoords,unit=Unit.MILES)
        print(f'starting point to {pickup} \n mileage is {fromStartMileage}\n')
        print(f'{pickup} to {dest}\n mileage is {deliveryMileage}')
        print()

def computeDistance(pos1, pos2):
    pos1Coords = parseCoords(pos1)
    pos2Coords = parseCoords(pos2)
    mileage = hs.haversine(pos1Coords, pos2Coords, unit=Unit.MILES)
    return mileage

def routeOrder(dels, start):
    bestMileage = None
    bestDel = None
    order = [((None, None, start), 0)]
    while dels != []:
        remainingDels = dels
        for (orderMileage, pickup, dest) in remainingDels:
            (_, _, currLoc), _ = order[-1]
            startMileage = computeDistance(currLoc, pickup)
            mileage = startMileage + orderMileage
            if bestMileage == None or mileage < bestMileage:
                bestMileage = mileage
                bestDel = (orderMileage, pickup, dest)
        order.append((bestDel, bestMileage))
        dels.remove(bestDel)
        
        bestMileage = None
    return order

def main():
    start = "28 Artist Drive Middle Island"
    dels = [("Chick Fil-A Port Jefferson NY", "Walmart Middle Island"), 
    ("261 Middle Country Rd, Selden, NY 11784", "6 Elkin Drive Middle Island NY"), ("1175 Middle Country Rd, Middle Island, NY 11953", 
    "17 Artist Lake Blvd")]
    #compute distances before routing
    for i in range(len(dels)):
        pickup, dest = dels[i]
        mileage = computeDistance(pickup, dest)
        dels[i] = (mileage, pickup, dest)
        

    return routeOrder(dels, start)
    
        
if __name__ == "__main__":
    print(main())






def slowerversion():
    start = "28 Artist Drive Middle Island"
    dels = [("Chick Fil-A Port Jefferson NY", "Walmart Middle Island"), 
    ("261 Middle Country Rd, Selden, NY 11784", "6 Elkin Drive Middle Island NY"), ("1175 Middle Country Rd, Middle Island, NY 11953", 
    "17 Artist Lake Blvd")]
    bestMileage = None
    bestDel = None
    order = [((None, start), 0)]
    while dels != []:
        remainingDels = dels
        for (pickup, dest) in remainingDels:
            (_, currLoc), _ = order[-1]
            startMileage = computeDistance(currLoc, pickup)
            endMileage = computeDistance(pickup, dest)
            mileage = startMileage + endMileage
            
            if bestMileage == None or mileage < bestMileage:
                bestMileage = mileage
                bestDel = (pickup, dest)
        order.append((bestDel, bestMileage))
        dels.remove(bestDel)
        
        bestMileage = None
    
    print(order)
        
