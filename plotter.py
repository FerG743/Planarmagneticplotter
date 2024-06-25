import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import argparse

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

    # Create a dictionary of results
    results = {
        'Bx': Bx,
        'By': By,
        'X': X,
        'Y': Y
    }

    return results

def plot_results(results):
    # Extract data from results
    B_magnitude = np.sqrt(results['Bx']**2 + results['By']**2)
    X = results['X']
    Y = results['Y']
    
    # Plot the results using inferno colormap
    plt.figure(figsize=(10, 8))
    plt.imshow(B_magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], origin='lower', cmap='inferno')
    plt.colorbar(label='Magnetic Field Strength (T)')
    plt.title('Magnetic Field Strength')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Magnetic Field Simulation')
    parser.add_argument('--config', type=str, help='Path to the configuration file')
    args = parser.parse_args()

    if args.config:
        # Batch mode
        with open(args.config, 'r') as f:
            config = json.load(f)
        results = run_simulation(config)
        # Save results or process them further as needed
    else:
        # Interactive mode
        config = {
            'current': float(input('Enter the current (A): ')),
            'n_turns': int(input('Enter the number of turns: ')),
            'conductor_thickness': float(input('Enter the conductor thickness (m): ')),
            'spacing_between_coils': float(input('Enter the spacing between coils (m): ')),
            'radius_coil': float(input('Enter the radius of the coil (m): ')),
            'central_gap_radius': float(input('Enter the central gap radius (m): ')),
            'num_points': int(input('Enter the number of points for the grid: '))
        }
        results = run_simulation(config)
        plot_results(results)

if __name__ == '__main__':
    main()
