from geopy.geocoders import Nominatim
import WazeRouteCalculator

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
            if ((bestDeliverBy == None and bestTime == None) or 
                (currTime < bestTime and currDeliverBy >= bestDeliverBy)):
                bestTime = currTime
                bestDeliverBy = currDeliverBy
                bestDel = (orderTime, pickup, dest, deliverBy)        
        
        beginTime += bestTime
        order.append((bestDel, bestTime, beginTime))
        dels.remove(bestDel)
        bestTime = None
        bestDeliverBy = None

    return order

def printResults(delOrder, beginTime):
    totalTime = 0
    startOrder = delOrder[0][0]
    print(f"\nOptimal order of delivery starting at {parseTime(beginTime)} at {startOrder[2]}:\n\nFirst, ")
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
    start = input("Enter starting address: ")
    beginTime = input("Enter the starting time: ")
    beginTime = timeToMins(beginTime)
    dels = []
    while True:
        storeAddress = input("Enter the store address for the order: ")
        if storeAddress == '':
            break
        houseAddress = input("Enter the house address for the order: ")
        deliverBy = input("Enter the time the order should be delivered by: ")
        deliverBy = timeToMins(deliverBy)
        print()
        print("Press enter once all orders have been fully entered.")
        dels.append((storeAddress, houseAddress, deliverBy))
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



