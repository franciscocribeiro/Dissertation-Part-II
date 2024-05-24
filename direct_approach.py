import pandas as pd
import matplotlib.pyplot as plt

# Define input parameters
salespeople = 2
compensation_per_salesperson = 100000
marketing_budget = 200000

# Revenue per project size
revenue_small = 75000
revenue_medium = 100000
revenue_large = 150000

# Project margin
margin = 0.3

# Project growth rate per year (e.g., 5% growth)
growth_rate = 0.05

# Support revenue rate and period
support_rate = 0.20
support_period = 5

# Scenarios
scenarios = {
    'Low': {'small': 3, 'medium': 1, 'large': 0.5},
    'Medium': {'small': 4, 'medium': 2, 'large': 0.5},
    'High': {'small': 5, 'medium': 2, 'large': 0.5}
}

# Calculate revenues and costs
def calculate_revenue_and_costs(scenario, years=4, growth_rate=0.05, support_rate=0.20, support_period=5):
    total_compensation = salespeople * compensation_per_salesperson
    revenues = []
    costs = []
    support_revenues = [0] * (years + 1)  # Initialize support revenue for each year

    for year in range(0, years + 1):  # Start from year 0
        growth_factor = (1 + growth_rate) ** year
        
        small_projects = scenario['small'] * salespeople * growth_factor if year > 0 else 0
        medium_projects = scenario['medium'] * salespeople * growth_factor if year > 0 else 0
        large_projects = scenario['large'] * salespeople * growth_factor if year > 0 else 0
        
        revenue = (small_projects * revenue_small +
                   medium_projects * revenue_medium +
                   large_projects * revenue_large)
        
        # Calculate support revenue from projects acquired in the current year
        support_revenue = (revenue * support_rate) / support_period
        # Add support revenue to the current and subsequent years within the support period
        for i in range(year, min(year + support_period, years + 1)):
            support_revenues[i] += support_revenue
        
        project_costs = revenue * (1 - margin)
        year_costs = total_compensation + project_costs
        
        if year == 0:
            year_costs += marketing_budget
        
        revenues.append(revenue + support_revenues[year])  # Add support revenue to total revenue
        costs.append(year_costs)
    
    return revenues, costs

# Calculate and store results
results = {}
for scenario_name, scenario in scenarios.items():
    revenues, costs = calculate_revenue_and_costs(scenario, growth_rate=growth_rate, support_rate=support_rate, support_period=support_period)
    results[scenario_name] = {'revenues': revenues, 'costs': costs}

# Convert results to DataFrame
years = [f'Year {i}' for i in range(0, 5)]
data = {
    'Year': years
}

for scenario_name, scenario_data in results.items():
    data[f'{scenario_name} Revenues'] = scenario_data['revenues']
    data[f'{scenario_name} Costs'] = scenario_data['costs']

df = pd.DataFrame(data)

# Plot the results
fig, axs = plt.subplots(3, 1, figsize=(10, 18), sharex=True)

for idx, scenario in enumerate(scenarios.keys()):
    axs[idx].plot(df['Year'], df[f'{scenario} Revenues'], label=f'{scenario} Revenues', color='blue')
    axs[idx].plot(df['Year'], df[f'{scenario} Costs'], label=f'{scenario} Costs', color='red')
    axs[idx].set_title(f'{scenario} Scenario')
    axs[idx].set_ylabel('Amount (£ in millions)')
    axs[idx].set_yscale('linear')
    axs[idx].legend()

axs[2].set_xlabel('Year')

plt.show()
