import pandas as pd
import matplotlib.pyplot as plt

# Direct Approach Parameters
salespeople_direct = 1  
compensation_per_salesperson = 100000
marketing_budget = 200000

# Revenue per project size
revenue_small_direct = 75000
revenue_medium_direct = 100000
revenue_large_direct = 150000

# Project margin
margin_direct = 0.3

# Project growth rate per year (e.g., 5% growth)
growth_rate_direct = 0.05

# Support revenue rate and period
support_rate_direct = 0.20
support_period_direct = 5

# Scenarios for Direct Approach
scenarios_direct = {
    'Low': {'small': 3, 'medium': 1, 'large': 0.5},
    'Medium': {'small': 4, 'medium': 2, 'large': 0.5},
    'High': {'small': 5, 'medium': 2, 'large': 0.5}
}

# Calculate revenues and costs for direct approach
def calculate_revenue_and_costs_direct(scenario, years=4, growth_rate=0.05, support_rate=0.20, support_period=5):
    total_compensation = salespeople_direct * compensation_per_salesperson
    revenues = []
    costs = []
    support_revenues = [0] * (years + 1)  # Initialize support revenue for each year

    for year in range(0, years + 1):  # Start from year 0
        growth_factor = (1 + growth_rate) ** year
        
        small_projects = scenario['small'] * salespeople_direct * growth_factor if year > 0 else 0
        medium_projects = scenario['medium'] * salespeople_direct * growth_factor if year > 0 else 0
        large_projects = scenario['large'] * salespeople_direct * growth_factor if year > 0 else 0
        
        revenue = (small_projects * revenue_small_direct +
                   medium_projects * revenue_medium_direct +
                   large_projects * revenue_large_direct)
        
        # Calculate support revenue from projects acquired in the current year
        support_revenue = (revenue * support_rate) / support_period
        # Add support revenue to the current and subsequent years within the support period
        for i in range(year, min(year + support_period, years + 1)):
            support_revenues[i] += support_revenue
        
        project_costs = revenue * (1 - margin_direct)
        year_costs = total_compensation + project_costs
        
        if year == 0:
            year_costs += marketing_budget
        
        revenues.append(revenue + support_revenues[year])  # Add support revenue to total revenue
        costs.append(year_costs)
    
    cumulative_revenues = pd.Series(revenues).cumsum().tolist()
    cumulative_costs = pd.Series(costs).cumsum().tolist()
    profitabilities = [r - c for r, c in zip(cumulative_revenues, cumulative_costs)]
    
    return revenues, costs, cumulative_revenues, cumulative_costs, profitabilities

# Calculate and store results for direct approach
results_direct = {}
for scenario_name, scenario in scenarios_direct.items():
    revenues, costs, cum_revenues, cum_costs, profits = calculate_revenue_and_costs_direct(
        scenario, growth_rate=growth_rate_direct, support_rate=support_rate_direct, support_period=support_period_direct)
    results_direct[scenario_name] = {
        'revenues': revenues,
        'costs': costs,
        'cumulative_revenues': cum_revenues,
        'cumulative_costs': cum_costs,
        'profitabilities': profits
    }


# Indirect Approach Parameters
salespeople_indirect = 1  
compensation_per_salesperson_indirect = 100000  
marketing_budget_indirect = 150000  

# Revenue per project size for indirect approach
revenue_small_indirect = 150000
revenue_medium_indirect = 200000
revenue_large_indirect = 300000

# Project margin for indirect approach
margin_indirect = 0.15

# Project growth rate per year (e.g., 6% growth) for indirect approach
growth_rate_indirect = 0.1

# Support revenue rate and period for indirect approach
support_rate_indirect = 0.2
support_period_indirect = 5

# Scenarios for Indirect Approach
scenarios_indirect = {
    'Low': {'small': 2, 'medium': 3, 'large': 3},
    'Medium': {'small': 3, 'medium': 4, 'large': 3},
    'High': {'small': 4, 'medium': 5, 'large': 4}
}

# Calculate revenues and costs for indirect approach
def calculate_revenue_and_costs_indirect(scenario, years=4, growth_rate=0.06, support_rate=0.18, support_period=4):
    total_compensation = salespeople_indirect * compensation_per_salesperson_indirect
    revenues = []
    costs = []
    support_revenues = [0] * (years + 1)  # Initialize support revenue for each year

    for year in range(0, years + 1):  # Start from year 0
        growth_factor = (1 + growth_rate) ** year
        
        small_projects = scenario['small'] * salespeople_indirect * growth_factor if year > 1 else 0
        medium_projects = scenario['medium'] * salespeople_indirect * growth_factor if year > 1 else 0
        large_projects = scenario['large'] * salespeople_indirect * growth_factor if year > 1 else 0
        
        revenue = (small_projects * revenue_small_indirect +
                   medium_projects * revenue_medium_indirect +
                   large_projects * revenue_large_indirect)
        
        # Calculate support revenue from projects acquired in the current year
        support_revenue = (revenue * support_rate) / support_period
        # Add support revenue to the current and subsequent years within the support period
        for i in range(year, min(year + support_period, years + 1)):
            support_revenues[i] += support_revenue
        
        project_costs = revenue * (1 - margin_indirect)
        year_costs = total_compensation + project_costs
        
        if year == 0:
            year_costs += marketing_budget_indirect
        
        revenues.append(revenue + support_revenues[year])  # Add support revenue to total revenue
        costs.append(year_costs)
    
    cumulative_revenues = pd.Series(revenues).cumsum().tolist()
    cumulative_costs = pd.Series(costs).cumsum().tolist()
    profitabilities = [r - c for r, c in zip(cumulative_revenues, cumulative_costs)]
    
    return revenues, costs, cumulative_revenues, cumulative_costs, profitabilities

# Calculate and store results for indirect approach
results_indirect = {}
for scenario_name, scenario in scenarios_indirect.items():
    revenues, costs, cum_revenues, cum_costs, profits = calculate_revenue_and_costs_indirect(
        scenario, growth_rate=growth_rate_indirect, support_rate=support_rate_indirect, support_period=support_period_indirect)
    results_indirect[scenario_name] = {
        'revenues': revenues,
        'costs': costs,
        'cumulative_revenues': cum_revenues,
        'cumulative_costs': cum_costs,
        'profitabilities': profits
    }


# Combine the results
combined_results = {}
for scenario_name in scenarios_direct.keys():  # Using direct approach scenarios as the key
    combined_results[scenario_name] = {
        'revenues': [d + i for d, i in zip(results_direct[scenario_name]['revenues'], results_indirect[scenario_name]['revenues'])],
        'costs': [d + i for d, i in zip(results_direct[scenario_name]['costs'], results_indirect[scenario_name]['costs'])],
        'cumulative_revenues': [d + i for d, i in zip(results_direct[scenario_name]['cumulative_revenues'], results_indirect[scenario_name]['cumulative_revenues'])],
        'cumulative_costs': [d + i for d, i in zip(results_direct[scenario_name]['cumulative_costs'], results_indirect[scenario_name]['cumulative_costs'])],
        'profitabilities': [d + i for d, i in zip(results_direct[scenario_name]['profitabilities'], results_indirect[scenario_name]['profitabilities'])]
    }

# Convert combined results to DataFrame
years = [f'Year {i}' for i in range(0, 5)]
combined_data = {
    'Year': years
}

for scenario_name, scenario_data in combined_results.items():
    combined_data[f'{scenario_name} Revenues'] = scenario_data['revenues']
    combined_data[f'{scenario_name} Costs'] = scenario_data['costs']

combined_df = pd.DataFrame(combined_data)
combined_df.to_csv('combined_results.csv')

# Plot the combined results
fig, axs = plt.subplots(3, 1, figsize=(10, 18), sharex=True)

for idx, scenario in enumerate(scenarios_direct.keys()):  # Using direct approach scenarios as the key
    axs[idx].plot(combined_df['Year'], combined_df[f'{scenario} Revenues'], label=f'{scenario} Revenues', color='blue')
    axs[idx].plot(combined_df['Year'], combined_df[f'{scenario} Costs'], label=f'{scenario} Costs', color='red')
    axs[idx].set_title(f'{scenario} Scenario')
    axs[idx].set_ylabel('Amount (£ in millions)')
    axs[idx].set_yscale('linear')
    axs[idx].legend()

axs[2].set_xlabel('Year')

plt.show()
