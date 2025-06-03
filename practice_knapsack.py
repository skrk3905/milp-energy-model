from pulp import LpProblem, LpVariable, LpMaximize

# 問題の定義（最大化）
prob = LpProblem("Simple_Knapsack", LpMaximize)

# 変数（0〜1の範囲）
x1 = LpVariable("x1", 0, 1)
x2 = LpVariable("x2", 0, 1)

# 目的関数（利益最大
prob += 60 * x1 + 100 * x2

# subject to
prob += 10 * x1 + 20 * x2 <= 50

prob.solve()

print("x1 =", x1.varValue)
print("x2 =", x2.varValue)