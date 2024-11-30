def calculate_fcf(data):
    print("Free Cash Flow (FCF) Calculator")
    data["fcf_list"] = []
    years = int(input("Enter the number of years: "))

    for year in range(1, years + 1):
        print(f"\n--- Year {year} ---")

        ebit = float(input("Enter EBIT: "))
        tax = float(input("Enter Tax (absolute value): "))
        depreciation_amortization = float(input("Enter Depreciation and Amortization: "))
        cap_ex = float(input("Enter Capital Expenditures (CapEx): "))
        change_in_ncwc = float(input("Enter Change in Non-Cash Working Capital: "))

        # Calculate FCF
        fcf = (ebit - tax) + depreciation_amortization - cap_ex - change_in_ncwc
        data["fcf_list"].append(fcf)

        print(f"FCF for Year {year}: {fcf:.2f}")

    print("\nSummary of FCF for all years:")
    for year, fcf in enumerate(data["fcf_list"], 1):
        print(f"Year {year}: {fcf:.2f}")


def calculate_wacc_and_terminal_value(data):
    print("\nWeighted Average Cost of Capital (WACC) and Terminal Value Calculator")

    # WACC Calculation Inputs
    data["risk_free_rate"] = float(input("Enter the 10-Year Treasury Rate (Risk-Free Rate) (e.g., 1.5 for 1.5%): ")) / 100
    data["beta"] = float(input("Enter the Beta of the company: "))
    data["market_return"] = float(input("Enter the expected Market Return (e.g., 10 for 10%): ")) / 100
    data["debt_value"] = float(input("Enter the total market value of debt: "))
    data["equity_value"] = float(input("Enter the total market value of equity: "))
    data["cost_of_debt"] = float(input("Enter the cost of debt (Rd) (e.g., 5 for 5%): ")) / 100
    data["tax_rate"] = float(input("Enter the corporate tax rate (e.g., 25 for 25%): ")) / 100

    # Calculate Cost of Equity using CAPM
    data["cost_of_equity"] = data["risk_free_rate"] + data["beta"] * (data["market_return"] - data["risk_free_rate"])
    total_value = data["debt_value"] + data["equity_value"]
    data["weight_of_debt"] = data["debt_value"] / total_value
    data["weight_of_equity"] = data["equity_value"] / total_value
    data["wacc"] = (
        data["weight_of_equity"] * data["cost_of_equity"]
        + data["weight_of_debt"] * data["cost_of_debt"] * (1 - data["tax_rate"])
    )

    # Intermediate WACC results
    print("\n--- WACC Results ---")
    print(f"Calculated Cost of Equity (Re): {data['cost_of_equity']:.4f} or {data['cost_of_equity'] * 100:.2f}%")
    print(f"Weighted Average Cost of Capital (WACC): {data['wacc']:.4f} or {data['wacc'] * 100:.2f}%")

    # EBITDA and Terminal Value
    data["ebit"] = float(input("\nEnter EBIT value: "))
    data["d_and_a"] = float(input("Enter Depreciation and Amortization value (D&A): "))
    data["ebitda"] = data["ebit"] + data["d_and_a"]
    print(f"Calculated EBITDA: {data['ebitda']:.2f}")

    # Exit Multiple Method
    data["exit_multiple"] = float(input("Enter the Exit Multiple: "))
    data["terminal_value_exit"] = data["ebitda"] * data["exit_multiple"]
    print(f"Terminal Value (Exit Multiple Method): {data['terminal_value_exit']:.2f}")

    # Perpetuity Growth Method
    data["perpetuity_growth_rate"] = float(input("\nEnter the Perpetuity Growth Rate (e.g., 3 for 3%): ")) / 100
    data["terminal_value_perpetuity"] = (
        data["ebitda"] * (1 - data["tax_rate"])
    ) / (data["wacc"] - data["perpetuity_growth_rate"])
    print(f"Terminal Value (Perpetuity Growth Method): {data['terminal_value_perpetuity']:.2f}")

    # Average of the Two Methods
    data["average_terminal_value"] = (
        data["terminal_value_exit"] + data["terminal_value_perpetuity"]
    ) / 2
    print(f"\n--- Final Results ---")
    print(f"Average Terminal Value: {data['average_terminal_value']:.2f}")


def discounting_factor(rate, periods):
    """Calculate the discounting factor."""
    return 1 / (1 + rate) ** periods


def calculate_enterprise_value(data):
    print("\nEnterprise Value (EV) Calculator")

    # Use FCF data
    cash_flows = data["fcf_list"]
    rate = float(input("Enter the discount rate (e.g., 8.49): ")) / 100
    terminal_value = data["average_terminal_value"]

    # Calculate discounting factors for all periods
    df_values = [discounting_factor(rate, period + 1) for period in range(len(cash_flows))]

    # Calculate PV of each cash flow
    pv_values = [cash_flows[i] * df_values[i] for i in range(len(cash_flows))]

    # Calculate PV of Terminal Value
    pv_terminal_value = terminal_value * df_values[-1]

    # Sum of PV of cash flows and PV of Terminal Value
    data["ev"] = sum(pv_values) + pv_terminal_value

    # Display results
    print("\nPresent Values of Cash Flows:")
    for period, pv in enumerate(pv_values, 1):
        print(f"Year {period}: ${pv:,.2f}")

    print(f"\nPresent Value of Terminal Value: ${pv_terminal_value:,.2f}")
    print(f"\nEnterprise Value (EV): ${data['ev']:,.2f}")


def calculate_equity_value_and_share_price(data):
    print("\nEquity Value and Share Price Calculator")

    # Equity Value Calculation
    cash = float(input("Enter Cash: "))
    short_term_debt = float(input("Enter Short-term Debt: "))
    long_term_debt = float(input("Enter Long-term Debt: "))
    marketable_securities = float(input("Enter Marketable Securities: "))

    # Net Debt
    net_debt = short_term_debt + long_term_debt - cash - marketable_securities
    data["equity_value"] = data["ev"] - net_debt

    # Display Equity Value
    print(f"\nEquity Value: ${data['equity_value']:,.2f}")

    # Share Price Calculation
    shares_outstanding = float(input("Enter Shares Outstanding: "))
    data["share_price"] = data["equity_value"] / shares_outstanding

    # Display Share Price
    print(f"Share Price: ${data['share_price']:.2f}")


# Main program
if __name__ == "__main__":
    data = {}
    calculate_fcf(data)
    calculate_wacc_and_terminal_value(data)
    calculate_enterprise_value(data)
    calculate_equity_value_and_share_price(data)
