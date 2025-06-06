from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary

facilities = ["A", "B","C", "D", "E"]
clients = ["1", "2", "3", "4"]

# 建設コスト
facility_cost = {"A": 120, "B": 100, "C": 110, "D": 130, "E": 90}
# 配送コスト
shipping_cost = {
    ("A", "1"): 20, ("A", "2"): 40, ("A", "3"): 60, ("A", "4"): 30,
    ("B", "1"): 35, ("B", "2"): 20, ("B", "3"): 25, ("B", "4"): 45,
    ("C", "1"): 50, ("C", "2"): 60, ("C", "3"): 20, ("C", "4"): 30,
    ("D", "1"): 25, ("D", "2"): 35, ("D", "3"): 45, ("D", "4"): 20,
    ("E", "1"): 30, ("E", "2"): 50, ("E", "3"): 40, ("E", "4"): 25
}

# 各施設の容量（最大供給量）
facility_cap = {"A": 80, "B": 50, "C": 60, "D": 70, "E": 40}

# 各需要地の需要量
client_demand = {"1": 30, "2": 40, "3": 20, "4": 30}

# 問題定義
prob = LpProblem("Facility_Loc", LpMinimize)

# 変数定義
# dictionary = {key: value for item in list}

# fを建設するか
x = {f: LpVariable(f"x_{f}", cat=LpBinary) for f in facilities}

# どのfがどのcにどの程度供給するか
y = {(f,c): LpVariable(f"y_{f}_{c}", cat="Continuous", lowBound=0) for f in facilities for c in clients}

# 目的関数:　Minimize 建設コスト＋配送コスト
prob += lpSum(facility_cost[f] * x[f] for f in facilities) +\
        lpSum(shipping_cost[f,c] * y[f,c] for f in facilities for c in clients)


# 制約①：すべての需要地が必ずどこか1つの施設から供給を受ける
for c in clients:
    prob += lpSum(y[f,c] for f in facilities) == client_demand[c]

# 制約②：各施設の供給量 ≤ 容量
for f in facilities:
        prob += lpSum(y[f,c] for c in clients) <= x[f] * facility_cap[f]

prob.solve()

print("----- 最適解 -----")
for f in facilities:
    print(f"Facility {f}: {'設置する' if x[f].varValue == 1 else '設置しない'}")
for f, c in y:
    if y[f, c].varValue > 0:
        print(f"Client {c} is served by Facility {f} with {y[f,c].varValue} units")
print("総コスト =", prob.objective.value())

import networkx as nx
import matplotlib.pyplot as plt

# グラフオブジェクト作成
G = nx.DiGraph()

# 施設ノード追加
# Node labels
for f in facilities:
    G.add_node(f"Facility {f}", color='lightgreen' if x[f].varValue == 1 else 'lightgray')

for c in clients:
    G.add_node(f"Client {c}", color='skyblue')

# 割当関係（エッジ）追加
for f, c in y:
    if y[f, c].varValue > 0:
        G.add_edge(f"Client {c}", f"Facility {f}", weight=y[f, c].varValue)

# ノードの色を取得
colors = [data['color'] for _, data in G.nodes(data=True)]

# レイアウトと描画
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1500, font_size=10, arrowsize=20)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): int(d['weight']) for u, v, d in G.edges(data=True)})

plt.title("Facility Assignment Graph")
plt.show()
