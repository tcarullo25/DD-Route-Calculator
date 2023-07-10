# DoorDash Route Calculator

This project implements a DoorDash route calculator that helps determine the optimal order of delivery for multiple orders. It utilizes the WazeRouteCalculator library to calculate the travel time between locations and optimize the delivery sequence.

## How it Works

1. **Starting Address**: The user enters the starting address for the delivery route and the desired starting time.
2. **Delivery Order**: The user enters the store address, house address, and the time by which each order should be delivered. The user can continue entering orders until all orders are fully entered.
3. **Time Conversion**: The delivery times are converted from hours and minutes format to minutes for easier calculation.
4. **Route Calculation**: The system calculates the travel time from the starting address to each pickup and delivery location using the WazeRouteCalculator library.
5. **Optimization**: The system determines the optimal order of delivery by considering the travel time and delivery time constraints for each order. It aims to minimize the total delivery time and ensure that orders are delivered on time.
6. **Results**: The system prints the optimal order of delivery, including the pickup and delivery locations, durations, delivery times, and finish time. The total delivery time and finish time are also displayed.

## Functions Overview

- `timeToMins(t)`: Converts time in hours and minutes format to minutes.
- `parseTime(mins)`: Converts minutes back to hours and minutes format for display.
- `computeRouteTime(pos1, pos2)`: Calculates the travel time between two locations using the WazeRouteCalculator library.
- `routeOrder(dels, start, beginTime)`: Determines the optimal order of delivery based on travel time and delivery time constraints.
- `printResults(delOrder, beginTime)`: Prints the results, including the optimal order of delivery, durations, delivery times, and finish time.
- `main()`: The main function that handles user input, calls the necessary functions, and displays the results.

Feel free to experiment with different starting addresses and delivery orders to optimize your DoorDash delivery route!

Note: The provided code is a simplified implementation and can be further optimized or enhanced for specific requirements.
