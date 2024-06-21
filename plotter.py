import re
import matplotlib.pyplot as plt

def read_results(file_path):
    distances = []
    field_values = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Extract distances and field values
            match = re.search(r'At (\d+\.\d+) mm: (\d+\.\d+) T', line)
            if match:
                distance = float(match.group(1))
                field_value = float(match.group(2)) * 1e6  # Convert from T to microtesla (μT)
                distances.append(distance)
                field_values.append(field_value)
    
    return distances, field_values

def plot_magnetic_field(distances, field_values):
    plt.figure(figsize=(10, 6))
    plt.plot(distances, field_values, marker='o', linestyle='-', color='b', label='Magnetic Field')

    plt.title('Magnetic Field Strength at Different Distances from Center')
    plt.xlabel('Distance from Center (mm)')
    plt.ylabel('Magnetic Field Strength (μT)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    file_path = 'simulation_results.txt'
    distances, field_values = read_results(file_path)
    plot_magnetic_field(distances, field_values)

if __name__ == '__main__':
    main()
