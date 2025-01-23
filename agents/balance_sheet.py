class BalanceSheet:
    def __init__(self):
        self.assets = {}
        self.liabilities = {}
        self.capital_stock = {}

    def add_asset(self, name, value):
        self.assets[name] = value

    def add_liability(self, name, value):
        self.liabilities[name] = value

    def add_capital_stock(self, name, value):
        self.capital_stock[name] = value

    def generate_report(self):
        report = "Balance Sheet Report\n"
        report += "====================\n\n"
        
        report += "Assets:\n"
        for name, value in self.assets.items():
            report += f"{name}: ${value}\n"
        report += "\n"

        report += "Liabilities:\n"
        for name, value in self.liabilities.items():
            report += f"{name}: ${value}\n"
        report += "\n"

        report += "Capital Stock:\n"
        for name, value in self.capital_stock.items():
            report += f"{name}: ${value}\n"
        report += "\n"

        total_assets = sum(self.assets.values())
        total_liabilities = sum(self.liabilities.values())
        total_capital_stock = sum(self.capital_stock.values())
        
        report += f"Total Assets: ${total_assets}\n"
        report += f"Total Liabilities: ${total_liabilities}\n"
        report += f"Total Capital Stock: ${total_capital_stock}\n"
        report += f"Net Worth: ${total_assets - total_liabilities}\n"

        return report

# Example usage:
# balance_sheet = BalanceSheet()
# balance_sheet.add_asset("Cash", 10000)
# balance_sheet.add_liability("Loan", 5000)
# balance_sheet.add_capital_stock("Common Stock", 2000)
# print(balance_sheet.generate_report())