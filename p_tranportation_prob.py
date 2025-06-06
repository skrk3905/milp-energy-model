from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary, LpStatus

# parameters
warehouses = ["W1", "W2", "W3"]
stores = ["S1", "S2", "S3", "S4"]
supply = {"W1": 70, "W2": 50, "W3": 30}
demand = {"S1": 40, "S2": 30, "S3": 20, "S4": 60}

cost = {
    "W1": {"S1": 2, "S2": 4, "S3": 5, "S4": 2},
    "W2": {"S1": 3, "S2": 1, "S3": 7, "S4": 6},
    "W3": {"S1": 4, "S2": 3, "S3": 4, "S4": 5}
}

# Decision variables
x = {(w, s): LpVariable(f"x_{w}_{s}", lowBound= 0, cat = "Continuous") for w in warehouses for s in stores}

# Problem definition
prob = LpProblem("Transportation_Prob", LpMinimize)

# Objective: minimize total cost
prob += lpSum(x[w,s] * cost[w][s] for w in warehouses for s in stores)

# === Constraints ===
# 1. Total amount from each warehouse must not exceed its supply
for w in warehouses:
    prob += lpSum(x[w, s] for s in stores) <= supply[w], f"SupplyLimit_{w}"

# 2. total amount delivered to each store must satisfy its demand
for s in stores:
    prob += lpSum(x[w,s] for w in warehouses) == demand[s], f"DemandSatisfies_{s}"

prob.solve()

print("---結果---")
print("status:", LpStatus[prob.status])

if prob.status == 1:  # Optimal
    for w in warehouses:
        for s in stores:
            if x[w,s].varValue > 0:
                print(f"warehouse {w} needs to send {x[w,s].varValue} units to store {s}.")
    
    print("Total Cost =", prob.objective.value())

else:
    print("No optimal solution was found.")