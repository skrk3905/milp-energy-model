from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, lpSum, LpBinary, LpStatus, value

# parameters
bento = ["A", "B"]
rice = {"A": 200, "B": 150}
people = {"A": 20, "B": 30}
profit = {"A": 200, "B": 300}

stock = 15 # kg
available_working = 10 # h

# Decision variables
x = {b: LpVariable(f"x_{b}", lowBound= 0, cat = "Integer") for b in bento}

# Problem definition
prob = LpProblem("Bento_Profit", LpMaximize)

# Objective
prob += lpSum(profit[b] * x[b] for b in bento)

# === Constraints ===
# 1. Total rice must not exceed the stock of rice
prob += lpSum(x[b] * rice[b] for b in bento) <= stock * 1000

# 2. Total working period must not exceed available labor hours
prob += lpSum(x[b] * people[b] for b in bento) <= available_working * 60

prob.solve()

print("--- Results ---")
print("status:", LpStatus[prob.status])

if prob.status == 1:
    for b in bento:
        print(f"Bento {b} should be made {x[b].varValue} units.")

    print(f"Total profit is {value(prob.objective)}yen.")
else:
    print("No optimal solution was found.")