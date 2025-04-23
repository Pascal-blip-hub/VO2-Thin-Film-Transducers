#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by Pascal J. Schroeder at INSP
"""

import numpy as np
from utils import create_directory, solve_simplified_integral, save_plot_data
import os

# =============================================================================
# CUSTOMIZABLE PARAMETERS - MODIFY THIS SECTION FOR YOUR SIMULATION
# =============================================================================

d = 100e-09          # VO2 coating thickness [m]
a_d_ratios = [1, 5, 10]  # List of a/d ratios to analyze where a correlates to gaussian beam width
log_start = -2       # Logarithmic min for rho values
log_stop = 2         # Logarithmic max for rho values
log_steps = 10000    # Number of steps
jobname = "Example_Name"  # Precise jobname (used for directory naming)

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def calculate_min_power(a_d_ratios, d, log_start, log_stop, log_steps, jobname):
    """Calculate minimum power values for multiple a/d ratios"""
    # Create directory structure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = create_directory(os.path.join(script_dir, jobname))
    data_dir = create_directory(os.path.join(base_dir, 'Data'))
    
    # Generate rho values
    rho_values = np.logspace(log_start, log_stop, log_steps)
    
    # Initialize results array
    results = np.zeros((len(rho_values), len(a_d_ratios) + 1))
    results[:, 0] = rho_values

    # Calculate for each a/d ratio
    for col, ratio in enumerate(a_d_ratios, 1):
        a = d * ratio
        results[:, col] = [solve_simplified_integral(a, d, rho) for rho in rho_values]

    # Save results
    output_path = os.path.join(data_dir, 'MIN_POWER_AD_RATIOS.txt')
    header = "rho" + "".join([f"\tpower_min_ad{ratio}" for ratio in a_d_ratios])
    save_plot_data(results, output_path, header=header)
    
    print(f"Results saved to: {output_path}")
    return results

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    results = calculate_min_power(
        a_d_ratios=a_d_ratios,
        d=d,
        log_start=log_start,
        log_stop=log_stop,
        log_steps=log_steps,
        jobname=jobname
    )
