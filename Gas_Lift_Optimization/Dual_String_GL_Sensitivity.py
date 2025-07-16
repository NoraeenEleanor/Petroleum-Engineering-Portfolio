" Dual String Gas Lift Sensitivity Analysis"

# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# Data Input: PVT, Well Test, Constraints
P_res_short = 1196  # psia
P_res_long = 1362   # psia
T_res_short = 128   # °F
T_res_long = 134    # °F
PI_short = 2.3      # STB/d/psi
PI_long = 2.05      # STB/d/psi
P_surface = 100     # psia

# Gas Injection Constraints
Gas_injection_surface = 1.7E06  # scf/d (approx 1.7 MMSCFD)

# Sensitivity Parameters
GIR_values = np.linspace(0.5E06, 3.0E06, 6)     # Gas Injection Rate (scf/d)
PI_values = np.linspace(0.8, 1.5, 5)            # Productivity Index (STB/d/psi)
Dome_values = np.linspace(1800, 2400, 4)        # Dome Pressure (psia)
DeltaP_valve_values = np.linspace(50, 300, 6)   # Pressure Drop (psia)

results = []

# Sensitivity Analysis
for GIR in GIR_values:
    for PI in PI_values:
        for DomeP in Dome_values:
            for DeltaP in DeltaP_valve_values:
                Q_liq_short = PI * (P_res_short - P_surface)
                Q_liq_long = PI * (P_res_long - P_surface)
                GLR_short = GIR / Q_liq_short
                GLR_long = GIR / Q_liq_long
                
                # Simplified energy efficiency model
                energy_efficiency = (GIR / (Q_liq_short + Q_liq_long)) * 0.85
                
                # CO2 emission estimation
                CO2_emission = GIR * 0.002  # metric tons/day
                
                # Economic value estimation
                oil_price = 65  # USD/bbl
                gas_price = 3.7  # USD per Mscf
                revenue = (Q_liq_short + Q_liq_long) * oil_price
                gas_cost = (GIR/1000) * gas_price
                profit =revenue - gas_cost
                
                results.append({
                    'GIR': GIR,
                    'PI': PI,
                    'DomeP': DomeP,
                    'DeltaP': DeltaP,
                    'Q_liq_short': Q_liq_short,
                    'Q_liq_long': Q_liq_long,
                    'Energy Efficiency': energy_efficiency,
                    'CO2_Emission': CO2_emission,
                    'Revenue': revenue,
                    'Gas_Cost': gas_cost,
                    'Profit': profit
                })

# Convert to DataFrame
df_results = pd.DataFrame(results)

# Save to CSV
df_results.to_csv('Gas_Lift_Sensitivity_Results.csv', index = False)

# Visualization - Sensitivity Plots
sns.set_style('whitegrid')

#Example: Profit vs. Gas Injection Rate
plt.figure(figsize=(10, 6))
sns.lineplot(x='GIR', y='Profit', data=df_results, hue = 'PI', palette='viridis')
plt.title('Profit vs Gas Injection Rate (by Productivity Index)')
plt.xlabel('Gas Injection Rate (scf/d)')
plt.ylabel('Profit (USD)')
plt.legend(title='Productivity Index')
plt.show()               