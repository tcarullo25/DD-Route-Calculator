import haversine as hs
from haversine import Unit
from geopy.geocoders import Nominatim
import WazeRouteCalculator
import time, datetime

def roundHalfUp(num):
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(num).to_integral_value(rounding=rounding))


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

def computeTime(pos1, pos2):
    region = 'US'
    vehicle_type = 'CAR'
    route = WazeRouteCalculator.WazeRouteCalculator(pos1, pos2, region, vehicle_type)
    time, _ = route.calc_route_info()
    return time

def routeOrder(dels, start):
    bestTime = None
    bestDel = None
    order = [((None, None, start), 0)]
    while dels != []:
        remainingDels = dels
        for (orderTime, pickup, dest) in remainingDels:
            (_, _, currLoc), _ = order[-1]
            startTime = computeTime(currLoc, pickup)
            currTime = startTime + orderTime
            #DEBUG
            #print(f'starting from {currLoc} start time {startTime} order time {orderTime}')
            #print(f'picking up from {pickup} to {dest}')
            if bestTime == None or currTime < bestTime:
                bestTime = currTime
                bestDel = (orderTime, pickup, dest)
            #print()
        #print()
        order.append((bestDel, bestTime))
        dels.remove(bestDel)
        
        bestTime = None
    return order

def printResults(delOrder):
    totalTime = 0
    startOrder = delOrder[0][0]
    print(f"Optimal order of delivery starting at {startOrder[2]}:\nFirst, ")
    lastOrder = delOrder[-1]
    delOrder = delOrder[1:-1]
    oldDest = startOrder[2]
    for ((_, pickup, dest), bestTime) in delOrder:
        totalTime += bestTime
        print(f'From {oldDest} -> {pickup} -> {dest}\nDuration: {roundHalfUp(bestTime)} mins\n')
        print("Then,")
        oldDest = dest
    (_, pickup, dest), bestTime = lastOrder
    bestTime += totalTime
    print(f"End off going from {oldDest} -> {pickup} -> {dest}\nDuration: {roundHalfUp(bestTime)} mins\n")
    print()  
    print(f"Total Time: {roundHalfUp(totalTime)} mins")
        


def main():
    start = "28 Artist Drive Middle Island"
    start_time_hour = int(time.strftime("%I", time.localtime()))
    start_time_min = int(time.strftime("%M", time.localtime()))
    start_time_sec = int(time.strftime("%S", time.localtime()))
    start_time = datetime.timedelta(hours=start_time_hour, minutes=start_time_min, seconds=start_time_sec)
    dels = [("Chick Fil-A Port Jefferson NY", "Walmart Middle Island"), 
    ("261 Middle Country Rd, Selden, NY 11784", "6 Elkin Drive Middle Island NY"), ("1175 Middle Country Rd, Middle Island, NY 11953", 
    "17 Artist Lake Blvd")]
    #compute times before routing
    for i in range(len(dels)):
        pickup, dest = dels[i]
        currTime = computeTime(pickup, dest)
        dels[i] = (currTime, pickup, dest)
    delOrder = routeOrder(dels, start)
    printResults(delOrder)

    
        
if __name__ == "__main__":
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    main()



