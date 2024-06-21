import numpy as np
from sklearn.linear_model import LinearRegression

# Step 1: Parse the Data from the Text File
def parse_simulation_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    config = {}
    results = {}

    for line in lines:
        line = line.strip()
        if line.startswith('Configuration:') or line.startswith('Results:'):
            continue
        elif line.startswith('  '):
            key, value = line.lstrip().split(': ')
            config[key] = float(value)
        elif line.startswith('    At'):
            _, distance, field = line.split(': ')
            distance = float(distance.split()[1])  # Extracting distance as float
            field = float(field.split()[0])  # Extracting field as float
            results[distance] = field
        else:
            key, value = line.split(': ')
            results[key] = float(value)

    return config, results

# Step 2: Prepare the Data for Training
def prepare_data(config, results):
    # Extracting relevant features and target for training
    conductor_thickness = config['conductor_thickness']
    spacing_between_coils = config['spacing_between_coils']
    radius_coil = config['radius_coil']
    central_gap_radius = config['central_gap_radius']

    # For simplicity, let's use the magnetic field at different distances as our target
    distances = list(results.keys())
    fields = list(results.values())

    X = np.array([conductor_thickness, spacing_between_coils, radius_coil, central_gap_radius]).reshape(1, -1)
    y = np.array(fields)

    return X, y

# Step 3: Train a Machine Learning Model
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

# Step 4: Generate a Coil with Specified Characteristics
def generate_coil(model, conductor_thickness, spacing_between_coils, radius_coil, central_gap_radius):
    # Prepare new input features for prediction
    X_new = np.array([conductor_thickness, spacing_between_coils, radius_coil, central_gap_radius]).reshape(1, -1)

    # Predict magnetic field
    predicted_field = model.predict(X_new)

    return predicted_field[0]

# Main function to run the entire process
def main():
    # Step 1: Parse the data
    file_path = 'simulation_data.txt'
    config, results = parse_simulation_data(file_path)

    # Step 2: Prepare data for training
    X, y = prepare_data(config, results)

    # Step 3: Train the model
    model = train_model(X, y)

    # Step 4: Generate a new coil with specified characteristics
    # Example characteristics of the new coil
    new_conductor_thickness = 0.0002
    new_spacing_between_coils = 0.0001
    new_radius_coil = 0.0015
    new_central_gap_radius = 0.0005

    predicted_field = generate_coil(model, new_conductor_thickness, new_spacing_between_coils,
                                   new_radius_coil, new_central_gap_radius)

    print(f"Predicted magnetic field for the new coil: {predicted_field:.6f} T")

if __name__ == "__main__":
    main()
