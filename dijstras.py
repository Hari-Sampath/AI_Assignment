import heapq

# Approximate road distances in km between major Indian cities
india_map = {
    "Delhi": {"Jaipur": 280, "Agra": 210, "Chandigarh": 250},
    "Jaipur": {"Delhi": 280, "Ahmedabad": 680, "Agra": 240},
    "Agra": {"Delhi": 210, "Jaipur": 240, "Lucknow": 330, "Gwalior": 120},
    "Lucknow": {"Agra": 330, "Varanasi": 320, "Patna": 530},
    "Ahmedabad": {"Jaipur": 680, "Mumbai": 520, "Pune": 660},
    "Mumbai": {"Ahmedabad": 520, "Pune": 150, "Hyderabad": 710, "Goa": 590},
    "Pune": {"Mumbai": 150, "Ahmedabad": 660, "Hyderabad": 590, "Goa": 430},
    "Goa": {"Mumbai": 590, "Pune": 430, "Bangalore": 560},
    "Hyderabad": {
        "Mumbai": 710,
        "Pune": 590,
        "Bangalore": 570,
        "Chennai": 630,
        "Nagpur": 500,
        "Visakhapatnam": 620,
    },
    "Nagpur": {"Hyderabad": 500, "Bhopal": 350, "Raipur": 280},
    "Bhopal": {"Nagpur": 350, "Gwalior": 430},
    "Gwalior": {"Agra": 120, "Bhopal": 430},
    "Bangalore": {"Hyderabad": 570, "Goa": 560, "Chennai": 350, "Kochi": 530},
    "Chennai": {"Hyderabad": 630, "Bangalore": 350, "Visakhapatnam": 800},
    "Visakhapatnam": {"Chennai": 800, "Bhubaneswar": 440, "Hyderabad": 620},
    "Bhubaneswar": {"Visakhapatnam": 440, "Kolkata": 440},
    "Kolkata": {"Bhubaneswar": 440, "Patna": 580},
    "Patna": {"Kolkata": 580, "Lucknow": 530, "Varanasi": 250},
    "Varanasi": {"Lucknow": 320, "Patna": 250},
    "Kochi": {"Bangalore": 530},
    "Chandigarh": {"Delhi": 250},
    "Raipur": {"Nagpur": 280},
}


def dijkstra_search(graph, start, goal):
    frontier = [
        (0, start, [])
    ]  # using priority queue as it can extract lowest distance for BFS easily

    # Explored set to keep track of the lowest cost found to reach each city, also holds distance to each city
    explored = {}

    while frontier:
        # Pop the city with the lowest cumulative cost
        current_cost, current_city, path = heapq.heappop(frontier)

        # If we reached our goal, we return the total cost and the path
        if current_city == goal:
            return current_cost, path + [current_city]

        # If we have already found a shorter path to this city, skip it
        if current_city in explored and explored[current_city] <= current_cost:
            continue

        # Mark the city as explored with its lowest cost
        explored[current_city] = current_cost

        # Expand neighbors
        for neighbor, distance in graph[current_city].items():
            new_cost = current_cost + distance

            # Only add to frontier if it's a new city or we found a cheaper route
            if neighbor not in explored or new_cost < explored[neighbor]:
                heapq.heappush(frontier, (new_cost, neighbor, path + [current_city]))

    return float("inf"), []  # Return infinity if no path is found


# sample values (can be made user inputted)
start_city = "Hyderabad"
destination_city = "Delhi"

total_distance, optimal_route = dijkstra_search(india_map, start_city, destination_city)

print(f"Optimal Route from {start_city} to {destination_city}:")
print(" -> ".join(optimal_route))
print(f"Total Driving Distance: {total_distance} km")
