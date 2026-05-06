import pandas as pd
import numpy as np
 
class YieldCurve:
    """
    Represents a financial yield curve for pricing and risk analysis.
    Provides methods to interpolate zero rates and compute discount factors.
    """
    def __init__(self, maturities, zero_rates, compounding="continous"):
        """
        Initialises the curve with market data.
        :param maturities: List or array of time to maturity (in years).
        :param rates: List or array of corresponding zero rates (as decimals).
        """
        self.maturities = np.array(maturities, dtype=float)
        self.zero_rates = np.array(zero_rates, dtype=float)
        self.compounding = compounding
 
        if len(self.maturities) != len(self.zero_rates):
            raise ValueError("Maturities and zero rates must have same length")
       
        order = np.argsort(self.maturities)
        self.maturities = self.maturities[order]
        self.zero_rates = self.zero_rates[order]
       
        # Create an interpolation function (Linear is standard for this task)
        # It allows us to find a rate for any T between our data points.
   
 
    def get_zero_rate(self, T):
        """
        Returns the interpolated zero rate for a given maturity T.
        """
        T = float(T)
        return float(np.interp(T, self.maturities, self.zero_rates))
 
    def get_discount_factor(self, T):
        """
        Computes the discount factor using continuous compounding: P(0,T) = e^(-rT).
        """
        z = self.get_zero_rate(T)
 
        if self.compounding == "continous":
            return np.exp(-z * T)
       
        elif self.compounding == "annual":
            return 1.0/ (1.0 + z) ** T
 
        else:
            raise ValueError("Unsupported compounding type")
 
    def plot(self, max_maturity=None):
 
        if max_maturity is None:
            T_grid = self.maturities
        else:
            T_grid = np.linspace(
                self.maturities.min(),
                max_maturity,
                100
            )
 
        z_grid = [self.get_zero_rate(T) for T in T_grid]
 
        plt.figure()
        plt.plot(T_grid, z_grid)
        plt.xlabel("Maturity (years)")
        plt.ylabel("Zero Rate")
        plt.title("Yield Curve")
        plt.grid()
        plt.show()
 