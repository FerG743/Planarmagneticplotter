# magnetic_field_simulation.py

import numpy as np

def magnetic_field_circular_loop(I, R, x, y, z=0):
    """
    Calculate the magnetic field at point (x, y, z) due to a circular loop of current I and radius R.
    """
    mu_0 = 4 * np.pi * 1e-7  # Permeability of free space (H/m)
    rho = np.sqrt(x**2 + y**2)
    z2 = z**2
    a2 = R**2
    denom = (rho**2 + z2 + a2)**1.5
    
    B_rho = mu_0 * I * R**2 / (2 * denom)  # radial component
    B_z = mu_0 * I * R**2 * z / denom      # z-component
    
    # Convert to Cartesian coordinates
    Bx = B_rho * x / rho
    By = B_rho * y / rho
    return Bx, By

def run_simulation(config):
    # Unpack configuration
    current = config['current']
    n_turns = config['n_turns']
    conductor_thickness = config['conductor_thickness']
    spacing_between_coils = config['spacing_between_coils']
    radius_coil = config['radius_coil']
    central_gap_radius = config['central_gap_radius']
    num_points = config['num_points']

    # Define the grid
    x = np.linspace(-radius_coil, radius_coil, num_points)
    y = np.linspace(-radius_coil, radius_coil, num_points)
    X, Y = np.meshgrid(x, y)

    # Initialize the magnetic field components
    Bx = np.zeros(X.shape)
    By = np.zeros(Y.shape)

    # Sum the magnetic field contributions from each turn
    for i in range(n_turns):
        r = central_gap_radius + i * (conductor_thickness + spacing_between_coils)
        Bx_contrib, By_contrib = magnetic_field_circular_loop(current, r, X, Y)
        Bx += Bx_contrib
        By += By_contrib

    # Calculate the magnitude of the magnetic field
    B_magnitude = np.sqrt(Bx**2 + By**2)

    # Calculate field at different distances
    center_index = num_points // 2
    distances = np.linspace(0, radius_coil, 10)  # 10 points from center to edge
    field_at_distances = []

    for dist in distances:
        idx = np.abs(x - dist).argmin()
        field_at_distances.append(B_magnitude[center_index, idx])

    # Calculate additional metrics
    max_field = np.max(B_magnitude)
    min_field = np.min(B_magnitude)
    mean_field = np.mean(B_magnitude)
    median_field = np.median(B_magnitude)
    std_dev_field = np.std(B_magnitude)

    # Create a dictionary of results
    results = {
        'config': config,
        'max_field': max_field,
        'min_field': min_field,
        'mean_field': mean_field,
        'median_field': median_field,
        'std_dev_field': std_dev_field,
        'distances': distances.tolist(),
        'field_at_distances': field_at_distances
    }

    return results