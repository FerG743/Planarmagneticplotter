# run_simulation.py

import argparse
import json
from magnetic_field_simulation import run_simulation

def get_config_from_user():
    config = {}
    config['current'] = float(input("Enter current (A): "))
    config['n_turns'] = int(input("Enter number of turns: "))
    config['conductor_thickness'] = float(input("Enter conductor thickness (m): "))
    config['spacing_between_coils'] = float(input("Enter spacing between coils (m): "))
    config['radius_coil'] = float(input("Enter coil radius (m): "))
    config['central_gap_radius'] = float(input("Enter central gap radius (m): "))
    config['num_points'] = int(input("Enter number of points for simulation: "))
    return config

def write_results_to_file(results, filename="simulation_results.txt"):
    with open(filename, 'w') as f:
        for i, result in enumerate(results, 1):
            f.write(f"Simulation {i}:\n")
            f.write(f"Configuration:\n")
            for key, value in result['config'].items():
                f.write(f"  {key}: {value}\n")
            f.write(f"Results:\n")
            f.write(f"  Max Field: {result['max_field']:.6f} T\n")
            f.write(f"  Min Field: {result['min_field']:.6f} T\n")
            f.write(f"  Mean Field: {result['mean_field']:.6f} T\n")
            f.write(f"  Median Field: {result['median_field']:.6f} T\n")
            f.write(f"  Standard Deviation: {result['std_dev_field']:.6f} T\n")
            f.write("  Magnetic field at different distances from center:\n")
            for dist, field in zip(result['distances'], result['field_at_distances']):
                f.write(f"    At {dist*1000:.2f} mm: {field:.6f} T\n")
            f.write("\n")

def main():
    parser = argparse.ArgumentParser(description="Run magnetic field simulation")
    parser.add_argument("--config", help="Path to configuration file")
    args = parser.parse_args()

    results = []

    if args.config:
        # Run simulation with configurations from file
        with open(args.config, 'r') as f:
            configurations = json.load(f)
        
        for config in configurations:
            results.append(run_simulation(config))
        
        print(f"Completed {len(configurations)} simulations.")
    else:
        # Run simulation with user input
        while True:
            config = get_config_from_user()
            results.append(run_simulation(config))
            
            if input("\nDo you want to run another simulation? (y/n): ").lower() != 'y':
                break

    # Write results to file
    write_results_to_file(results)
    print(f"Results have been written to simulation_results.txt")

if __name__ == "__main__":
    main()