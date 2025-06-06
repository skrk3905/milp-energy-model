import pulp as pl

# ----------------------------
# Parameters
# ----------------------------
D = 10000            # annual electricity demand[kwh/y]
CF_PV = 0.14          # PV capacity factor
hours_year = 24 * 365 # Hours in one year
CRF = 0.10            # Capital recovery factor

C_PV_cap  = 120_000   # PV capital cost [JPY/kW]
C_Bat_cap =  40_000   # Battery capital cost [JPY/kWh]  (not yet beneficial)
C_grid    =      25   # Grid electricity price [JPY/kWh]

# ----------------------------
# Model definition
# ----------------------------
model = pl.LpProblem("Simple_DES_Design", pl.LpMinimize)

# Decision variables
x_pv  = pl.LpVariable("PV_capacity_kW", lowBound=0)       # kW
x_bat = pl.LpVariable("Battery_capacity_kWh", lowBound=0) # kWh
E_imp = pl.LpVariable("Grid_import_kWh", lowBound=0)      # kWh / year

# Derived PV generation (kWh / year)
E_pv = CF_PV * hours_year * x_pv

# Objective: annualized total cost (≈ numerator of LCOE)
annual_cost = CRF * (C_PV_cap * x_pv + C_Bat_cap * x_bat) + C_grid * E_imp
model += annual_cost

# Constraint: annual energy balance
model += E_pv + E_imp == D, "Annual_energy_balance"

# ----------------------------
# Solve the model
# ----------------------------
model.solve(pl.PULP_CBC_CMD(msg=False))
model.solve(pl.PULP_CBC_CMD(msg=False)) # Using solver of Coin-or Branch and Cut and no log output

# ----------------------------
# Results
# ----------------------------
print(f"PV capacity  [kW]  : {x_pv.value():8.3f}")
print(f"Battery cap. [kWh] : {x_bat.value():8.3f}")
print(f"Grid import [kWh]  : {E_imp.value():8.1f}")
print(f"Total PV generation [kWh] : {E_pv.value():8.1f}")
print(f"Annual cost [JPY]  : {pl.value(annual_cost):,.0f}")