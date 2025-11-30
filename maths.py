import numpy as np
import matplotlib.pyplot as plt
import time
import sys

# Define set S = open unit disk
def in_S(z):
    return abs(z) < 1

# Test point type
def classify_point(z0, epsilon_values=[0.1, 0.05, 0.01,0.2]):
    results = []
    for eps in epsilon_values:
        # Sample neighborhood
        theta = np.linspace(0, 2*np.pi, 100)
        neighborhood = z0 + eps * np.exp(1j*theta)
        
        in_S_count = sum(1 for z in neighborhood if in_S(z))
        out_S_count = sum(1 for z in neighborhood if not in_S(z))
        
        results.append((eps, in_S_count, out_S_count))
    
    # Classify
    all_in = all(out == 0 for _, _, out in results)
    all_out = all(in_count == 0 for _, in_count, _ in results)
    mixed = not all_in and not all_out
    
    if all_in:
        return "Interior"
    elif all_out:
        return "Exterior"
    else:
        return "Boundary"

# Test points
test_points = {
    "z = 0": 0 + 0j,
    "z = 0.5": 0.5 + 0j,
    "z = 0.95": 0.95 + 0j,
    "z = 1": 1 + 0j,
    "z = 1.05": 1.05 + 0j,
    "z = 2": 2 + 0j
}

for label, z in test_points.items():
    classification = classify_point(z)
    print(f"{label}: {classification}")

# Visualize
fig, ax = plt.subplots(figsize=(10, 10))

# Draw set S
theta = np.linspace(0, 2*np.pi, 100)
S_boundary = np.exp(1j*theta)
ax.plot(S_boundary.real, S_boundary.imag, 'b-', linewidth=3, label='Boundary of S')
ax.fill(S_boundary.real, S_boundary.imag, alpha=0.2, color='blue', label='Set S (interior)')

# Mark points
colors = {'Interior': 'green', 'Exterior': 'red', 'Boundary': 'orange'}
for label, z in test_points.items():
    classification = classify_point(z)
    ax.plot(z.real, z.imag, 'o', markersize=12, 
            color=colors[classification], label=f'{label} ({classification})')

ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title('Interior, Boundary, and Exterior Points')
plt.show()

time.sleep(20)
sys.exit("Hope you've gained something")