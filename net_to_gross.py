from scipy.optimize import minimize
import math

def calculate_pension(basic, housing_allowance, transport_allowance):
    """
    Calculate the pension contribution based on basic salary and allowances.

    Args:
        basic (float): Basic salary portion of the gross income.
        housing_allowance (float): Housing allowance.
        transport_allowance (float): Transport allowance.

    Returns:
        float: The total pension contribution.
    """
    # Pension is calculated as 8% of basic, housing, and transport allowances
    return 0.08 * basic + 0.08 * housing_allowance + 0.08 * transport_allowance

def calculate_paye_tax(gross_income, pension):
    """
    Calculate the PAYE (Pay As You Earn) tax based on gross income and pension contribution.

    Args:
        gross_income (float): Total gross income.
        pension (float): Pension contribution deducted from the gross income.

    Returns:
        float: The total PAYE tax.
    """
    # Calculate contributions for CRF (Contributory Relief Fund) and GRF (General Relief Fund)
    CRF = max(0.01 * gross_income, 200000)
    GRF = 0.2 * gross_income
    
    # Taxable income is gross income minus CRF, GRF, and pension contributions
    taxable_income = gross_income - CRF - GRF - pension

    # Calculate PAYE tax based on taxable income brackets
    tax = 0.07 * min(300000, taxable_income) + \
          0.11 * min(300000, max(taxable_income - 300000, 0)) + \
          0.15 * min(500000, max(taxable_income - 600000, 0)) + \
          0.19 * min(500000, max(taxable_income - 1100000, 0)) + \
          0.21 * min(1600000, max(taxable_income - 1600000, 0)) + \
          0.24 * max(0, taxable_income - 3200000)
    return tax

def calculate_gross_from_net(net_income, housing_allowance, transport_allowance, other_allowances):
    """
    Determines the gross income from net income using optimization to minimize the objective function.

    Args:
        net_income (float): The net income entered by the user.
        housing_allowance (float): Housing allowance.
        transport_allowance (float): Transport allowance.
        other_allowances (dict): A dictionary containing other allowances.

    Returns:
        float: The estimated gross income calculated by minimizing the difference between computed and actual net income.
    """
    # Define the objective function for optimization
    def objective_function(gross):
        # Calculate total allowances and basic salary
        total_allowances = sum(other_allowances.values()) + housing_allowance + transport_allowance
        # basic = gross[0] - total_allowances
        basic = 0.5 * gross[0] # (CHECK: as suggested by the accounting expert)
        
        # Calculate pension and PAYE tax based on gross income
        pension = calculate_pension(basic, housing_allowance, transport_allowance)
        paye_tax = calculate_paye_tax(gross[0], pension)
        
        # The objective function to minimize: the square of the difference between actual net income and calculated net
        return math.pow(( gross[0] - net_income - pension - paye_tax ), 2)
    
    # Initial guess for the optimizer
    initial_guess = [net_income * 1.4]
    # print(f"Initial guess is {initial_guess}")
    
    # Perform the optimization to minimize the objective function
    result = minimize(objective_function, initial_guess, method='SLSQP', bounds=[(net_income, None)])
    
    # Check if optimization was successful and return the estimated gross income
    if result.success:
        return result.x[0]
    else:
        raise ValueError("Optimization did not converge")
    
    
if __name__ == "__main__":

    # Example inputs

    housing_allowance = 30000
    transport_allowance = 5000
    other_allowances = {
        "Education": 10000,
        "Incentive": 8000,
        "Productivity": 6000,
        "Non-Strike": 4000,
        "Performance": 12000
    }

    net_income = 1600000

    # Calculate gross from net
    gross = calculate_gross_from_net(net_income, housing_allowance, transport_allowance, other_allowances)
    pension = calculate_pension(basic=.5*gross, housing_allowance=housing_allowance, transport_allowance=transport_allowance)
    paye = calculate_paye_tax(gross, pension)
    print(f'The initial net value is {net_income:,.2f}')
    print(f'The gross value for net = N{net_income:,.2f} is = N{gross:,.2f}')
    print(f"Pension value is N{round(pension, 2):,.2f}")
    print(f"PAYE Tax is {round(paye, 2):,.2f}")
    print(f"New Net value is {round(gross - paye - pension):,.2f}")

