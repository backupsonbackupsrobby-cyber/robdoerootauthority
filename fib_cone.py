import math

def generate_fibonacci_cone_points(num_points=72, height=10.0, max_radius=5.0):
    golden_ratio = (1 + math.sqrt(5)) / 2
    points = []
    
    for i in range(num_points):
        z = i / (num_points - 1) * height
        radius = (1.0 - (i / num_points)) * max_radius
        theta = 2 * math.pi * i / (golden_ratio ** 2)
        
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((round(x, 3), round(y, 3), round(z, 3)))
        
    return points

points = generate_fibonacci_cone_points()
print(f"Generated {len(points)} nodes mapped across the Fibonacci cone lattice.")
for p in points[:5]:
    print(f"Node Coordinate: {p}")
