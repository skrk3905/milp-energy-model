from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary, LpStatus

# parameter
sources =["solar", "wind", "diesel"] # list
cost = {"solar": 0, "wind": 1, "diesel": 5} # dictionary
cap = {"solar": 50, "wind": 80, "diesel": 100} 
demand = 130

# Problem definition
prob = LpProblem("Energy_Dispatch", LpMinimize) 

# Decision variables (electricity generation per source)
gen = {s: LpVariable(f"gen_{s}", lowBound= 0, cat = "Continuous") for s in sources}

# Objective: minimize total cost
prob += lpSum(cost[s] * gen[s] for s in sources)

# === Constraints ===
# 1: total generation must meet demand
prob += lpSum(gen[s] for s in sources) == demand, "DemandConstraint"

# 2: generation must not exceed cap
for s in sources:
    prob += gen[s] <= cap[s], f"MaxGen_{s}"

prob.solve()

print("----- 結果 -----")
print("Status:", LpStatus[prob.status])

if prob.status == 1:  # Optimal
    for s in sources:
        print(f"{s}を{gen[s].varValue}kW発電させる")
else:
    print("最適解が見つかりませんでした。")