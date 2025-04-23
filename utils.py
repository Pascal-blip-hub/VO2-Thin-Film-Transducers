# utils.py - Core utility functions
import numpy as np
import os
from scipy import integrate, special

def get_filename(prefix, rho, power=None, suffix='txt'):
    """Generate standardized filenames"""
    if power is not None:
        return f"{prefix}_RHO{rho}_P{power}.{suffix}"
    else:
        return f"{prefix}_RHO{rho}.{suffix}"

def create_directory(directory_path):
    """Create directory if it doesn't exist"""
    os.makedirs(directory_path, exist_ok=True)
    return directory_path

def save_plot_data(data, filename, header=None):
    """Save data to a text file with optional header"""
    with open(filename, 'w') as file:
        if header:
            file.write(header + "\n")
        for row in data:
            file.write("\t".join(map(str, row)) + "\n")

def integrand(xi, R, a, d, rho):
    """Integrand function for analytical calculation"""
    return ((rho + np.tanh(xi * d / a)) / (1 + rho * np.tanh(xi * d / a))) * \
           special.j0(xi * R / a) * np.exp(-xi**2 / 8)

def solve_integral(R, a, d, rho):
    """Solve the integral for a given R, a, d, and rho"""
    result, _ = integrate.quad(integrand, 0, np.inf, args=(R, a, d, rho))
    return 1 / result

def simplified_integrand(xi, a, d, rho):
    """Simplified integrand for minimum power calculation"""
    return ((rho + np.tanh(xi * d / a)) / (1 + rho * np.tanh(xi * d / a))) * \
            np.exp(-xi**2 / 8)

def solve_simplified_integral(a, d, rho):
    """Solve the simplified integral for minimum power calculation"""
    result, _ = integrate.quad(simplified_integrand, 0, np.inf, args=(a, d, rho))
    return 1 / result

