# simulate_wbc_response.py
# 🔬 RBDC Phase 1 – WBC Migration Simulation
# Simulates chemoattractant diffusion from capsule & shows WBC activation zone

import numpy as np
import matplotlib.pyplot as plt

Q = 1e-9  # mol
D = 1e-6  # cm^2/s
t = 600   # seconds
threshold = 1e-8  # mol/cm^3

r_values = np.linspace(0.001, 1.5, 500)
def concentration(r, Q, D, t):
    return (Q / (4 * np.pi * D * t)) * np.exp(-r**2 / (4 * D * t))

C_values = concentration(r_values, Q, D, t)
activation_radius = r_values[np.where(C_values < threshold)[0][0]]

plt.figure(figsize=(10, 6))
plt.plot(r_values * 10, C_values, label='Concentration Profile', color='blue')
plt.axhline(threshold, color='red', linestyle='--', label='WBC Activation Threshold')
plt.axvline(activation_radius * 10, color='green', linestyle='--', label=f'Activation Radius ≈ {activation_radius*10:.2f} mm')
plt.xlabel("Distance from Capsule (mm)")
plt.ylabel("Concentration (mol/cm³)")
plt.title("RBDC Simulation – WBC Attractant Concentration Field")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

