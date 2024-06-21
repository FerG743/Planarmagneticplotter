import random

def generate_config():
  """Generates a single configuration dictionary."""
  current = random.uniform(0.1, 1.0)  # Current between 0.5 and 3.0
  n_turns = random.randint(20, 40)  # Turns between 20 and 40
  conductor_thickness = random.uniform(0.000089, 0.00025)  # Thickness between 0.089mm and 0.25mm
  spacing_between_coils = random.uniform(0.000089, conductor_thickness)  # Spacing less than thickness
  radius_coil = random.uniform(conductor_thickness * 5, 0.01)  # Radius larger than everything else
  central_gap_radius = random.uniform(0.000089, radius_coil - conductor_thickness)  # Gap less than radius - thickness
  num_points = 700  # Fixed number of points

  return {
      "current": current,
      "n_turns": n_turns,
      "conductor_thickness": conductor_thickness,
      "spacing_between_coils": spacing_between_coils,
      "radius_coil": radius_coil,
      "central_gap_radius": central_gap_radius,
      "num_points": num_points
  }

# Generate 100 configurations
configs = [generate_config() for _ in range(100)]

# Write the configurations to a file (replace "config.json" with your desired filename)
with open("config.json", "w") as f:
  import json
  json.dump(configs, f, indent=2)  # Pretty print for readability

print("Generated 100 configurations and saved to config.json")
