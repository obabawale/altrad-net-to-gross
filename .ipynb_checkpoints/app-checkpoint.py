import math


def calculate_pension(gross_income):
    """Calculate pension 

    Args:
      gross_income: Gross Income is a floating point value

    Returns: float: returns a pension which is a floating point value
    """
    pass


def calculate_paye_tax(gross_income):
    """Calculate Gross Income"""

    def calculate_taxable_income(gross_income):
        """Calculate taxable income"""
        pass

    return calculate_taxable_income(gross_income)


def calculcate_gross_from_net(gross_income: float, **kwargs):
    """Determine the gross income fron net using a minimization function"""
    if not gross_income:
        raise ValueError("Please provide ")

    net_income = kwargs.get('net_income')

    LHS = net_income
    RHS = gross_income - \
        calculate_pension(gross_income) - calculate_paye_tax(gross_income)
    return math.pow((LHS - RHS), 2)


def main():
    housing = int(input("Enter housing allowance "))
    transport = int(input("Enter transport allowance "))
    print(f"Housing allowance is {housing}")
    print(f"Transport allowance is {transport}")


if __name__ == "__main__":
    main()
