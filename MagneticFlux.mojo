from math import pi, sqrt, pow

struct Vector2D:
    var x: Float64
    var y: Float64

    fn __init__(inout self, x: Float64, y: Float64):
        self.x = x
        self.y = y

struct Array2D:
    var data: DynamicVector[Float64]
    var rows: Int
    var cols: Int

    fn __init__(inout self, rows: Int, cols: Int):
        self.rows = rows
        self.cols = cols
        self.data = DynamicVector[Float64](rows * cols)
        for i in range(rows * cols):
            self.data.append(0.0)

    fn __getitem__(self, row: Int, col: Int) -> Float64:
        return self.data[row * self.cols + col]

    fn __setitem__(inout self, row: Int, col: Int, value: Float64):
        self.data[row * self.cols + col] = value

fn magnetic_field_circular_loop(I: Float64, R: Float64, x: Float64, y: Float64, z: Float64 = 0) -> Vector2D:
    let mu_0 = 4 * pi * 1e-7
    let rho = sqrt(x*x + y*y)
    let z2 = z*z
    let a2 = R*R
    let denom = pow(rho*rho + z2 + a2, 1.5)
    
    let B_rho = mu_0 * I * R*R / (2 * denom)
    let B_z = mu_0 * I * R*R * z / denom
    
    let Bx = B_rho * x / rho if rho > 0 else 0
    let By = B_rho * y / rho if rho > 0 else 0
    return Vector2D(Bx, By)

fn print_magnetic_field_summary(Bx: Array2D, By: Array2D):
    var min_magnitude = Float64.max
    var max_magnitude = 0.0
    var center_magnitude = 0.0
    var corner_magnitude = 0.0
    var edge_magnitude = 0.0

    let num_points = Bx.rows
    
    for i in range(num_points):
        for j in range(num_points):
            let magnitude = sqrt(Bx[i, j] * Bx[i, j] + By[i, j] * By[i, j])
            if magnitude < min_magnitude:
                min_magnitude = magnitude
            if magnitude > max_magnitude:
                max_magnitude = magnitude
            
            if i == num_points // 2 and j == num_points // 2:
                center_magnitude = magnitude
            elif i == 0 and j == 0:
                corner_magnitude = magnitude
            elif i == num_points // 2 and j == num_points - 1:
                edge_magnitude = magnitude

    print("Magnetic Field Summary:")
    print("Minimum magnitude: ", min_magnitude, " T")
    print("Maximum magnitude: ", max_magnitude, " T")
    print("Magnitude at center: ", center_magnitude, " T")
    print("Magnitude at corner: ", corner_magnitude, " T")
    print("Magnitude at edge: ", edge_magnitude, " T")

fn main():
    # Define constants and parameters
    let current: Float64 = 1
    let n_turns: Int = 22
    let conductor_thickness: Float64 = 0.152e-3
    let spacing_between_coils: Float64 = 0.152e-3
    let radius_coil: Float64 = 5e-3
    let central_gap_radius: Float64 = 2.3e-3

    let num_points: Int = 700
    let step: Float64 = 2 * radius_coil / (num_points - 1)

    var Bx = Array2D(num_points, num_points)
    var By = Array2D(num_points, num_points)

    for i in range(num_points):
        for j in range(num_points):
            let x = -radius_coil + i * step
            let y = -radius_coil + j * step
            
            var Bx_total: Float64 = 0
            var By_total: Float64 = 0

            for k in range(n_turns):
                let r = central_gap_radius + k * (conductor_thickness + spacing_between_coils)
                let B = magnetic_field_circular_loop(current, r, x, y)
                Bx_total += B.x
                By_total += B.y

            Bx[i, j] = Bx_total
            By[i, j] = By_total

    print("Magnetic field calculation completed.")
    print_magnetic_field_summary(Bx, By)

main()