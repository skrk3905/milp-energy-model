import pulp as pl

def run_case(params):
# ----------------------------
# Parameters
# ----------------------------
    # --- unpack paramters
    D = params["D"]                 # annual electricity demand[kwh/y]
    CF_PV = params["CF_PV"]         # PV capacity factor
    C_grid = params["C_grid"]
    C_PV_cap = params["C_PV_cap"]   # PV capital cost [JPY/kW]
    C_Bat_cap = params["C_Bat_cap"] # Battery capital cost [JPY/kWh]
    P_exp = params["P_exp"]         # feed-in tariff [JPY/kWh]

    # --- Constant parameters
    hours_year = 24 * 365 # Hours in one year
    eta_c = 0.95  # charging efficiency
    eta_d = 0.95  # discharging efficiency

    # --- model
    m = pl.LpProblem("Simple_DES_Design", pl.LpMinimize)

    # variables
    x_pv  = pl.LpVariable("PV_kW", lowBound=0)       # kW
    x_bat = pl.LpVariable("Battery_kWh", lowBound=0) # kWh
    E_imp = pl.LpVariable("Grid_imp", lowBound=0)      # kWh / year
    E_exp = pl.LpVariable("Grid_exp", lowBound=0)      # surplus PV sold [kWh / year]
    E_bat_c = pl.LpVariable("Battery_chg", lowBound=0)  # annual charging energy
    E_bat_d = pl.LpVariable("Battery_dis", lowBound=0)  # annual discharging energy

    # pv generation
    E_pv = CF_PV * hours_year * x_pv # Derived PV generation (kWh / year)

    # Objective: cost
    CRF = params["CRF"] # Capital recovery factor
    cost = CRF * (C_PV_cap * x_pv + C_Bat_cap * x_bat) + C_grid * E_imp - P_exp * E_exp
    m += cost

    # Constraint
    m += E_pv + E_imp + E_bat_d == D + E_bat_c + E_exp
    m += E_bat_c <= eta_c * x_bat
    m += E_bat_d <= eta_d * x_bat
    m += E_bat_d <= eta_d * E_bat_c
    m += E_exp <= E_pv
    # solve
    m.solve(pl.PULP_CBC_CMD(msg=False))
    return{
        "status": pl.LpStatus[m.status],
        "PV_kW":  x_pv.value(),
        "Bat_kWh":x_bat.value(),
        "Grid_imp":E_imp.value(),
        "Cost_JPY":pl.value(cost)
    }

# --- quick test
base = {
    # --- demand & resource ---
    "D"       : 10_000,   # kWh/year  (≈ 3一般家庭分)
    "CF_PV"   : 0.13,     # capacity factor (13%)
    # --- economics ---
    "CRF"     : 0.0802,   # r=5%, n=20y
    "C_PV_cap": 120_000,  # JPY/kW
    "C_Bat_cap": 40_000,  # JPY/kWh
    "eta_c"   : 0.95,     # charge efficiency
    "eta_d"   : 0.95,     # discharge efficiency
    "P_exp"   : 10,       # JPY/kWh (feed-in tariff)
}

grid_prices = [5, 8, 9, 10, 25, 40]   # JPY/kWh
for Cg in grid_prices:
    res  = run_case(base | {"C_grid": Cg})
    print(f"Cost of Grid={Cg} → PV={res['PV_kW']:.2f} kW, Bat={res['Bat_kWh']:.2f} kWh, Cost={res['Cost_JPY']:.0f}")

"""
# ----------------------------
# Results
# ----------------------------
print("--- Results ---")
print("status:", pl.LpStatus[model.status])

if model.status == 1:
    print(f"PV capacity  [kW]  : {x_pv.value():8.3f}")
    print(f"Battery cap. [kWh] : {x_bat.value():8.3f}")
    print(f"Grid import [kWh]  : {E_imp.value():8.1f}")
    print(f"Grid export [kWh] : {E_exp.value():8.1f}")
    print(f"Total PV generation [kWh] : {E_pv.value():8.1f}")
    print(f"Annual cost [JPY]  : {annual_cost.value():8.1f}")
    print(f"Battery charge [kWh] : {E_bat_c.value():8.1f}")
    print(f"Battery discharge[kWh]: {E_bat_d.value():8.1f}")

else:
    print("No optimal solution was found.") 
"""