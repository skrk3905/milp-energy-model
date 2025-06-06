from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary, LpStatus, value

# parameters
energy_center = ["C1", "C2", "C3"]
village = ["V1", "V2", "V3", "V4"]
max_supply = {"C1": 80, "C2": 100, "C3": 60}
required_demand = {"V1": 50, "V2": 40, "V3": 60, "V4": 60}
cost = {
    "C1":{"V1": 4, "V2": 6, "V3": 9, "V4": 7},
    "C2":{"V1": 5, "V2": 4, "V3": 7, "V4": 6},
    "C3":{"V1": 8, "V2": 7, "V3": 6, "V4": 5}
}

# Decision Variables
x = {(c, v): LpVariable(f"x_{c}_{v}", lowBound= 0) for c in energy_center for v in village}
y = {(c, v): LpVariable(f"y_{c}_{v}", cat = "Binary") for c in energy_center for v in village}

# Problem Definition
prob = LpProblem("Energy_Cost_Minimize", LpMinimize)

# Objective
prob += lpSum(x[c, v] * cost[c][v] for c in energy_center for v in village)

# === Constraints ===
# 1. Each village's demand must be fully met
for v in village:
    prob += lpSum(x[c, v] for c in energy_center) == required_demand[v]

# 2. Total supply from each energy center must not exceed its capacity
for c in energy_center:
    prob += lpSum(x[c, v] for v in village) <= max_supply[c]

# 3. C3 can supply energy to only one village
prob += lpSum(y["C3", v] for v in village) <= 1

# 4. V4 must be supplied by more than two centers
prob += lpSum(y[c, "V4"] for c in energy_center) >= 2

# 5. Each individual supply must be limited by the demand and activation status
for c in energy_center:
    for v in village:
        prob += x[c, v] <= required_demand[v] * y[c, v]

# yが1のとき、必ず供給させる
epsilon = 1
for c in energy_center:
    for v in village:
        prob += x[c, v] >= epsilon * y[c, v]

prob.solve()

print("--- Results ---")
print("status:", LpStatus[prob.status])

if prob.status == 1:
    for c in energy_center:
        for v in village:
            if x[c, v].varValue > 0:
                print(f"Energy Center {c} provides {x[c, v].varValue} kWh to village {v}.")

    print(f"Total cost is {value(prob.objective)}yen.")
else:
    print("No optimal solution was found.")