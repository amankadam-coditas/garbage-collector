```bash

Problem Statement: 

"Smart Garbage Collection & Tracking System"
Background
City authorities want to optimize garbage collection. Some bins overflow quickly, while others stay half-empty for days. Trucks waste time following fixed routes, leading to fuel costs and complaints from citizens.
You are tasked to build the backend for a Smart Garbage Management System that:
Keeps track of bins placed across the city.
Decides when bins need pickup.
Assigns trucks to collect garbage efficiently.



Requirements
Bin Tracking
Each bin is uniquely identified.
It should have information like where it is placed and how much garbage it can hold.
Garbage level in a bin will change over time (e.g., sensors can update it).
If a bin goes above 80% of its capacity, it should be marked for pickup.
 Hint: You’ll need to store some state about bins and their fill levels.

Truck Assignment
There are multiple garbage trucks in the system.
Each truck can only carry a certain amount of garbage in one trip.
Your service should be able to assign flagged bins to trucks without overloading them.  
 Hint: Think about matching bins (with weights) to trucks (with capacity).

Pickup Scheduling


Provide an endpoint that lists all bins that are currently pending pickup.
Provide another endpoint that assigns those bins to available trucks.
Hint: You’ll need to relate bins and trucks dynamically, not just store them separately.



Insights


An endpoint that shows which areas of the city are producing the most garbage in the last 7 days.
This can help authorities place more bins where needed.
Hint: Keep track of historical fill level changes or pickups.

Expected Deliverables
REST APIs(Primary)
Data stored in a database(Primary)
Minimal API docs
Logging and Exception Handling(Secondary)
Authentication(Secondary)



Evaluation Criteria
Correctness: Does it meet the functional requirements?


Design: How clean is the API and database design?


Efficiency: Is truck assignment handled logically?
```