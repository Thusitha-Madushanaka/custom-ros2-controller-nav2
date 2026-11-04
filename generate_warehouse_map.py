import os

# Warehouse dimensions: 30 m x 24 m
resolution = 0.05

xmin, xmax = -15.0, 15.0
ymin, ymax = -12.0, 12.0

width = int((xmax - xmin) / resolution)
height = int((ymax - ymin) / resolution)

# Occupancy values:
# 254 = free
# 0   = occupied
grid = [[254 for _ in range(width)] for _ in range(height)]

# Obstacle definitions:
# (center_x, center_y, size_x, size_y)
obstacles = [
    # Warehouse boundary walls
    (0.0, 12.0, 30.0, 0.2),
    (0.0, -12.0, 30.0, 0.2),
    (15.0, 0.0, 0.2, 24.0),
    (-15.0, 0.0, 0.2, 24.0),

    # Storage racks
    (-7.0, 7.0, 6.0, 0.8),
    (5.0, 7.0, 6.0, 0.8),
    (-7.0, -7.0, 6.0, 0.8),
    (5.0, -7.0, 6.0, 0.8),

    # Pallets
    (-10.0, 1.5, 0.9, 0.9),
    (10.0, -1.5, 0.9, 0.9),
    (0.0, 9.0, 0.9, 0.9),
]

# Convert world coordinates into occupancy-grid cells
for row in range(height):
    for col in range(width):

        x = xmin + (col + 0.5) * resolution
        y = ymax - (row + 0.5) * resolution

        for cx, cy, sx, sy in obstacles:
            if (abs(x - cx) <= sx / 2 and
                    abs(y - cy) <= sy / 2):
                grid[row][col] = 0
                break

# Save map files
map_directory = os.path.expanduser("~/nav2_ws/maps")
os.makedirs(map_directory, exist_ok=True)

map_path = os.path.join(
    map_directory, "ciima_warehouse.pgm"
)

yaml_path = os.path.join(
    map_directory, "ciima_warehouse.yaml"
)

with open(map_path, "w") as f:
    f.write(f"P2\n{width} {height}\n255\n")
    for row in grid:
        f.write(" ".join(map(str, row)) + "\n")

with open(yaml_path, "w") as f:
    f.write(
        "image: ciima_warehouse.pgm\n"
        "mode: trinary\n"
        f"resolution: {resolution}\n"
        f"origin: [{xmin}, {ymin}, 0.0]\n"
        "negate: 0\n"
        "occupied_thresh: 0.65\n"
        "free_thresh: 0.25\n"
    )

print("CIIMA warehouse map generated successfully!")
print(f"Dimensions: {width} x {height} cells")
print(f"Physical size: {xmax-xmin} m x {ymax-ymin} m")
print(f"Resolution: {resolution} m/pixel")
print(f"Map saved: {map_path}")
