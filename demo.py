data = {
    "bins": [
        {
            "id": 1,
            "total_capacity": 100,
            "is_available": True,
            "fill_level": 81,
            "name": "Bin-A",
            "location_id": 1
        },
        {
            "id": 3,
            "total_capacity": 100,
            "is_available": True,
            "fill_level": 95,
            "name": "Bin-DZ",
            "location_id": 3
        },
        {
            "id": 7,
            "total_capacity": 100,
            "is_available": True,
            "fill_level": 95,
            "name": "Bin-DZZ",
            "location_id": 3
        }
    ],
    "trucks": [
        {
            "fill_level": 0,
            "id": 1,
            "name": "Truck-A",
            "total_capacity": 200,
            "is_available": True
        },
        {
            "fill_level": 0,
            "id": 2,
            "name": "Truck-B",
            "total_capacity": 300,
            "is_available": True
        },
        {
            "fill_level": 0,
            "id": 3,
            "name": "Truck-K",
            "total_capacity": 400,
            "is_available": True
        },
        {
            "fill_level": 0,
            "id": 4,
            "name": "Truck-Y",
            "total_capacity": 100,
            "is_available": True
        }
    ]
}

for bin in data["bins"]:
    print(bin["fill_level"], bin["total_capacity"])
    for truck in data["trucks"]:
        current_capacity_of_truck = truck["total_capacity"] - truck["fill_level"] 
        if current_capacity_of_truck >= bin["fill_level"]:
            truck["fill_level"] += bin["fill_level"]
            bin["fill_level"] = 0
            bin["is_available"] = False
        elif current_capacity_of_truck < bin["fill_level"]:
            truck["fill_level"] = truck["total_capacity"]
            bin["fill_level"] -= current_capacity_of_truck
print(data)
