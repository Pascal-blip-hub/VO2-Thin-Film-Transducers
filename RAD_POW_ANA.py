import numpy as np
import os
from utils import create_directory, solve_integral, save_plot_data

# =============================================================================
# CUSTOMIZABLE PARAMETERS - MODIFY THIS SECTION FOR YOUR SIMULATION
# =============================================================================

a = 1000e-09         # Gaussian beam width parameter (smearing measure) [m]
d = 100e-09          # VO2 coating thickness [m]
T_0 = 341            # Transition temperature VO2 [K]
r_min = 0.0          # Minimum normalized radius
r_max = 5.0          # Maximum normalized radius
r_steps = 100        # Number of radius steps
rho_values = [0.5]   # List of rho values to analyze
jobname = "analytical_job"  # Precise jobname (used for directory naming)

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def batch_rho_analysis(rho_values, a, d, r_min, r_max, r_steps, jobname):
    """Run analytical analysis for multiple rho values and save results"""
    # Create directory structure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = create_directory(os.path.join(script_dir, jobname))
    data_dir = create_directory(os.path.join(base_dir, 'Data'))
    
    # Generate normalized radius values
    radius_norm = np.linspace(r_min, r_max, r_steps)
    results = {}

    for rho in rho_values:
        print(f"\n--- Analyzing Rho = {rho} ---")
        power_norm = [solve_integral(R * a, a, d, rho) for R in radius_norm]
        results[rho] = {
            'power_norm': power_norm,
            'radius_norm': radius_norm
        }

    # Save data in consistent format
    output_path = os.path.join(data_dir, 'RAD_POW_ANALYTICAL.txt')
    data_to_save = np.column_stack((radius_norm, *[results[rho]['power_norm'] for rho in rho_values]))
    header = "radius_norm" + "".join([f"\tpower_rho{rho}" for rho in rho_values])
    save_plot_data(data_to_save, output_path, header=header)
    
    return output_path

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    output_path = batch_rho_analysis(
        rho_values=rho_values,
        a=a,
        d=d,
        r_min=r_min,
        r_max=r_max,
        r_steps=r_steps,
        jobname=jobname
    )
    print(f"Results saved to: {output_path}")
