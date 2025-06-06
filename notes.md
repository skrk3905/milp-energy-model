
# Memo: Simple DES model in `r_ver1`

## Objective of the Model
- To determine the optimal PV capacity and grid import to meet the annual electricity demand $ D $ [kWh].
- Battery is not used due to non-merit.
- The goal is to minimize the total annualized cost.

## Parameter Settings

| Parameter   | Description                    | Value     |
|-------------|--------------------------------|-----------|
| D           | Annual electricity demand [kWh]| 10,000    |
| CF_PV       | PV capacity factor             | 0.14      |
| hours_year  | Total hours per year           | 8,760     |
| CRF         | Capital Recovery Factor        | 0.10      |
| C_PV_cap    | PV capital cost [JPY/kW]       | 120,000   |
| C_grid      | Grid electricity price [JPY/kWh]| 25       |

## Model Behavior

### Theoretical Optimal PV size:
$$
x_{\text{pv}} = \frac{D}{CF \times 8760} = \frac{10,000}{0.14 \times 8760} \approx 8.154 \text{ [kW]}
$$

### Annual cost comparison:
- PV: $ 120{,}000 \times 8.154 \times 0.10 \approx 97{,}800 $ JPY
- Grid-only: $ 25 \times 10{,}000 = 250{,}000 $ JPY

→ PV is more cost-effective, so **grid import = 0** is chosen as the optimal solution.