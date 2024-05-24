import pandas as pd
import matplotlib.pyplot as plt

# Define input parameters for partnership strategy
salesperson_compensation = 100000
marketing_budget = 150000

# Revenue per project size
revenue_small = 150000
revenue_medium = 200000
revenue_large = 300000

# Project margin for partnership
margin = 0.15

# Project growth rate per year (e.g., 5% growth)
growth_rate = 0.10

# Support revenue rate and period
support_rate = 0.20
support_period = 5

# Scenarios for partnership strategy
scenarios = {
    'Low': {'small': 2, 'medium': 3, 'large': 3},
    'Medium': {'small': 3, 'medium': 4, 'large': 3},
    'High': {'small': 4, 'medium': 5, 'large': 4}
}

# Calculate revenues and costs for partnership strategy
def calculate_revenue_and_costs(scenario, years=4, growth_rate=0.05, support_rate=0.20, support_period=5):
    total_compensation = salesperson_compensation
    revenues = []
    costs = []
    support_revenues = [0] * (years + 1)  # Initialize support revenue for each year

    for year in range(0, years + 1):  # Start from year 0
        growth_factor = (1 + growth_rate) ** year
        
        small_projects = scenario['small'] * growth_factor if year > 1 else 0
        medium_projects = scenario['medium'] * growth_factor if year > 1 else 0
        large_projects = scenario['large'] * growth_factor if year > 1 else 0
        
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
    
    cumulative_revenues = pd.Series(revenues).cumsum().tolist()
    cumulative_costs = pd.Series(costs).cumsum().tolist()
    profitabilities = [r - c for r, c in zip(cumulative_revenues, cumulative_costs)]
    
    return revenues, costs, cumulative_revenues, cumulative_costs, profitabilities

# Calculate and store results for partnership strategy
results = {}
for scenario_name, scenario in scenarios.items():
    revenues, costs, cum_revenues, cum_costs, profits = calculate_revenue_and_costs(
        scenario, growth_rate=growth_rate, support_rate=support_rate, support_period=support_period)
    results[scenario_name] = {
        'revenues': revenues,
        'costs': costs,
        'cumulative_revenues': cum_revenues,
        'cumulative_costs': cum_costs,
        'profitabilities': profits
    }

# Convert results to DataFrame
years = [f'Year {i}' for i in range(0, 5)]
data = {
    'Year': years
}

for scenario_name, scenario_data in results.items():
    data[f'{scenario_name} Revenues'] = scenario_data['revenues']
    data[f'{scenario_name} Costs'] = scenario_data['costs']

df = pd.DataFrame(data)

# Plot the results for partnership strategy
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

# Output the cumulative results for analysis
results_df = pd.DataFrame(results)
results_df
