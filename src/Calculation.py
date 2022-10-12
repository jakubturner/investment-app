class Calculation:
    """this class is use for calculate compound investments"""
    def __init__(self, money, years, interest) -> None:
        self.money = money
        self.years = years
        self.interest = interest

    @classmethod
    def calculate_result(cls, money: str, years: str, interest: str) -> str:
        """this class method calculate concrete investment calculation"""
        raw_calc = int(money) * (1 + float(interest) / 100) ** float(years)
        return "{:.2f}".format(raw_calc)
