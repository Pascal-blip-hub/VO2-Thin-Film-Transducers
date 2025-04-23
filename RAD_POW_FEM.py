import mph
import numpy as np
import os
from utils import create_directory, save_plot_data, get_filename

# =============================================================================
# CUSTOMIZABLE PARAMETERS - MODIFY THIS SECTION FOR YOUR SIMULATION
# =============================================================================

a = 1e-7                  # Gaussian beam width parameter (smearing measure) [m]
T_0 = 341                 # Transition temperature VO2 [K]
model_path = "250000x250000nm_SYMMETRIC_MIN500_NARROW10"  # Path to COMSOL model file (with or without .mph)
rho_values = [0.5]        # List of rho values to analyze
power_min = 0             # Minimum power value
power_max = 0.0075        # Maximum power value
power_steps = 3           # Number of power steps
jobname = "Test123"        # Precise jobname (used for directory naming)
cores = 24                # Number of CPU cores to use for COMSOL

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def R(filename, temperature_threshold, y_tolerance=1e-9):
    """
    Reads data from a file and returns the first R coordinate where
    Temperature just exceeds the specified threshold for a specific Y value.
    Returns NaN if no such R is found.
    """
    try:
        data = np.loadtxt(filename, skiprows=8)
        R = data[:, 0]
        Y = data[:, 1]
        Temperature = data[:, 2]
        y_value = np.max(Y)
        Y_filter = np.isclose(Y, y_value, atol=y_tolerance)
        R_filtered = R[Y_filter]
        Temperature_filtered = Temperature[Y_filter]
        positive_R_filter = R_filtered >= 0
        R_filtered = R_filtered[positive_R_filter]
        Temperature_filtered = Temperature_filtered[positive_R_filter]
        filtered_data = np.column_stack((R_filtered, Temperature_filtered))
        sorted_data = filtered_data[np.argsort(filtered_data[:, 1])]
        for r, temp in sorted_data:
            if temp > temperature_threshold:
                return r
        return np.nan
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return np.nan
    except Exception as e:
        print(f"An error occurred: {e}")
        return np.nan

def initialize_comsol(comsol_model_path, cores=24):
    """
    Initialize COMSOL client and load model.
    Returns the client and model objects.
    """
    try:
        client = mph.start(cores=cores)
        if not comsol_model_path.endswith('.mph'):
            comsol_model_path += '.mph'
        model = client.load(comsol_model_path)
        return client, model
    except Exception as e:
        print(f"Error initializing COMSOL: {e}")
        return None, None

def run_analysis_with_model(model, rho_v, power_values, T_0, a, k_sub=None, save_dir='Data', jobname="job"):
    """Run comprehensive thermal analysis for a given rho value"""
    # Set default k_sub if not provided
    if k_sub is None:
        k_sub = ((3.6 + 6) / 2) / rho_v

    # Create directory structure
    rawsolved_dir = create_directory(os.path.join(save_dir, 'RAWSOLVED'))
    rho_subfolder_path = create_directory(os.path.join(rawsolved_dir, f'RHO_{rho_v}'))
    plot_data_dir = create_directory(os.path.join(save_dir, 'PLOTDATA'))

    # Set common parameters in the model
    model.parameter('a', a)
    model.parameter('T_0', T_0)
    model.parameter('k_si', k_sub)
    model.parameter('rho', rho_v)

    for power in power_values:
        model.parameter('p_laser', power)
        print(f"Rho: {rho_v}, Power: {power}")
        model.build()
        model.solve('Study 1')
        filename = get_filename('SOLVED', rho_v, power)
        model.export('Plot 1', os.path.join(rho_subfolder_path, filename))

    # TEMP-EVAL AT SURFACE AND SPOT SIZE DETERMINATION
    results = []
    for power in power_values:
        filename = os.path.join(rho_subfolder_path, get_filename('SOLVED', rho_v, power))
        results.append(R(filename, temperature_threshold=T_0))
    r = np.array(results) * 1e-9
    P = power_values
    P_ref = float(rho_v * k_sub * (T_0 - 293.15) * 2 * np.pi * a)
    P_norm = np.array(P) / P_ref
    r_norm = np.abs(r / a)
    COMSOL_data_path = os.path.join(plot_data_dir, f'RAD_POW_RHO{rho_v}_COMSOL.txt')
    data_to_save = np.column_stack((P_norm, r_norm))
    save_plot_data(data_to_save, COMSOL_data_path, header="q_norm\tr_norm")
    return {'P_norm': P_norm, 'r_norm': r_norm}

def batch_rho_analysis(rho_values, power_values, comsol_model_path, jobname, a, T_0, cores=24):
    """Run analysis for multiple rho values with specified power values"""
    # Create main job directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = create_directory(os.path.join(script_dir, jobname))
    data_dir = create_directory(os.path.join(base_dir, 'Data'))
    results = {}
    client, model = initialize_comsol(comsol_model_path, cores)
    if client is None or model is None:
        print("Failed to initialize COMSOL. Aborting batch analysis.")
        return None
    for rho in rho_values:
        print(f"\n--- Analyzing Rho = {rho} ---")
        result = run_analysis_with_model(
            model,
            rho_v=rho,
            power_values=power_values,
            a=a,
            T_0=T_0,
            save_dir=data_dir,
            jobname=jobname
        )
        if result is not None:
            results[rho] = result
    return results

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    power_values = np.linspace(power_min, power_max, power_steps)
    results = batch_rho_analysis(
        rho_values=rho_values,
        power_values=power_values,
        comsol_model_path=model_path,
        jobname=jobname,
        a=a,
        T_0=T_0,
        cores=cores
    )
