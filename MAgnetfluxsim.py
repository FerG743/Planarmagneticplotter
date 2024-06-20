import numpy as np
import matplotlib.pyplot as plt

# Define constants
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space (H/m)

# Coil parameters
current = 1  # Amperes
n_turns = 22
conductor_thickness = 0.152e-3  # meters
spacing_between_coils = 0.152e-3  # meters
radius_coil = 5e-3  # meters
central_gap_radius = 2.3e-3  # meters

# Define the number of points in the grid
num_points = 700
x = np.linspace(-radius_coil, radius_coil, num_points)
y = np.linspace(-radius_coil, radius_coil, num_points)
X, Y = np.meshgrid(x, y)

# Initialize the magnetic field components
Bx = np.zeros(X.shape)
By = np.zeros(Y.shape)

# Function to calculate the magnetic field from a circular loop
def magnetic_field_circular_loop(I, R, x, y, z=0):
    """
    Calculate the magnetic field at point (x, y, z) due to a circular loop of current I and radius R.
    """
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

# Sum the magnetic field contributions from each turn
for i in range(n_turns):
    r = central_gap_radius + i * (conductor_thickness + spacing_between_coils)
    Bx_contrib, By_contrib = magnetic_field_circular_loop(current, r, X, Y)
    Bx += Bx_contrib
    By += By_contrib

# Calculate the magnitude of the magnetic field
B_magnitude = np.sqrt(Bx**2 + By**2)

# Plot the magnetic field magnitude
plt.figure(figsize=(8, 8))
plt.contourf(X * 1e3, Y * 1e3, B_magnitude, levels=100, cmap='inferno')
plt.colorbar(label='Magnetic Field Strength (T)')
plt.title('Magnetic Field Distribution in the Plane of the Coil')
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.axis('equal')
plt.grid(True)
plt.show()
