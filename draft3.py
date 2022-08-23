import haversine as hs
from haversine import Unit
from geopy.geocoders import Nominatim
import WazeRouteCalculator
import time
from datetime import timedelta, datetime

def roundHalfUp(num):
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(num).to_integral_value(rounding=rounding))

def timeToMins(t):
   split = t.split(":")
   timeInfo = 60 * int(split[0]) + int(split[1])
   return timeInfo

def parseTime(mins):
    hours = roundHalfUp(mins//60)
    minutes = roundHalfUp(mins % 60)
    if minutes < 10:
        minutes = f'0{minutes}'
    if hours > 12:
        hours = f'{hours-12}'
    return f'{hours}:{minutes}'

def computeRouteTime(pos1, pos2):
    region = 'US'
    vehicle_type = 'CAR'
    route = WazeRouteCalculator.WazeRouteCalculator(pos1, pos2, region, vehicle_type)
    time, _ = route.calc_route_info()
    return time

def routeOrder(dels, start, beginTime):
    bestTime = None
    bestDel = None
    bestDeliverBy = None
    order = [((None, None, start, None), 0, None)]
    while dels != []:
        remainingDels = dels
        for (orderTime, pickup, dest, deliverBy) in remainingDels:
            (_, _, currLoc, _), _, _= order[-1]
            startTime = computeRouteTime(currLoc, pickup)
            currTime = startTime + orderTime
            currDeliverBy = abs(deliverBy - (beginTime + currTime))
            print(currDeliverBy, pickup)
            #DEBUG
            #print(f'starting from {currLoc} start time {startTime} order time {orderTime}')
            #print(f'picking up from {pickup} to {dest}')
            if ((bestDeliverBy == None and bestTime == None) or 
                (currTime < bestTime and currDeliverBy >= bestDeliverBy)):
                bestTime = currTime
                bestDeliverBy = currDeliverBy
                bestDel = (orderTime, pickup, dest, deliverBy)
                #deliver by : 1:40 begin: 12:30 timeTaken: 30
        print()
        
        
        beginTime += bestTime
        order.append((bestDel, bestTime, beginTime))
        dels.remove(bestDel)
        bestTime = None
        bestDeliverBy = None

    return order

def printResults(delOrder, beginTime):
    totalTime = 0
    startOrder = delOrder[0][0]
    print(f"Optimal order of delivery starting at {parseTime(beginTime)} at {startOrder[2]}:\n\nFirst, ")
    lastOrder = delOrder[-1]
    delOrder = delOrder[1:-1]
    oldDest = startOrder[2]
    for ((_, pickup, dest, deliverBy), bestTime, finishTime) in delOrder:
        totalTime += bestTime
        deliverBy = parseTime(deliverBy)
        finishTime = parseTime(finishTime)
        print(f'from {oldDest} -> {pickup} -> {dest}\nDuration: {roundHalfUp(bestTime)} mins')
        print(f'Deliver By: {deliverBy}\nFinish at: {finishTime}\n')
        print("Then,")
        oldDest = dest
    (_, pickup, dest, deliverBy), bestTime, finishTime = lastOrder
    deliverBy = parseTime(deliverBy)
    finishTime = parseTime(finishTime)
    totalTime += bestTime
    print(f"end off going from {oldDest} -> {pickup} -> {dest}\nDuration: {roundHalfUp(bestTime)} mins")
    print(f'Deliver By: {deliverBy}\nFinish at: {finishTime}\n')
    print(f"Total Time: {roundHalfUp(totalTime)} mins\nFinish at: {finishTime}")
        

def main():
    start = "28 Artist Drive Middle Island"
    beginTime = timeToMins('12:31')
    delTime1 = timeToMins('12:50')
    delTime2 = timeToMins('1:10')
    delTime3 = timeToMins('1:05')
    dels = [("Chick Fil-A Port Jefferson NY", "Walmart Middle Island", delTime1), 
    ("261 Middle Country Rd, Selden, NY 11784", "6 Elkin Drive Middle Island NY", delTime2), ("1175 Middle Country Rd, Middle Island, NY 11953", 
    "17 Artist Lake Blvd", delTime3)]
    #compute times before routing
    for i in range(len(dels)):
        pickup, dest, deliverBy = dels[i]
        orderTime = computeRouteTime(pickup, dest)
        dels[i] = (orderTime, pickup, dest, deliverBy)
    delOrder = routeOrder(dels, start, beginTime)
    printResults(delOrder, beginTime)

    
        
if __name__ == "__main__":
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    main()



