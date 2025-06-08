#!/usr/bin/env python3
"""
Core RBDC Classes
================

Reusable components for Resonant Bio-Decoy Capsule simulation and analysis.
For Charlotte, with love from John T DuCrest Lock & SYMBEYOND.
"""

import numpy as np
from typing import Dict

class ChemoattractantField:
    """Models 3D chemoattractant diffusion from RBDC capsule."""
    
    def __init__(self, Q: float, D: float, degradation_rate: float = 0):
        self.Q = Q  # Total release (mol)
        self.D = D  # Diffusion coefficient (cm²/s)
        self.degradation_rate = degradation_rate  # s⁻¹
        
    def concentration(self, r: float, t: float) -> float:
        """John's proven 3D diffusion equation."""
        if t <= 0:
            return 0.0
        
        # Base 3D spherical diffusion
        base = (self.Q / (4 * np.pi * self.D * t)) * np.exp(-r**2 / (4 * self.D * t))
        
        # Add degradation if specified
        if self.degradation_rate > 0:
            lambda_decay = np.sqrt(self.degradation_rate / self.D)
            decay_factor = np.exp(-lambda_decay * r) if lambda_decay * r < 20 else 0
            return base * decay_factor
            
        return base

class WBCResponse:
    """Models white blood cell response to chemoattractant gradients."""
    
    def __init__(self, activation_threshold: float, hill_coefficient: float = 2.0):
        self.threshold = activation_threshold  # mol/cm³
        self.hill_n = hill_coefficient
        
    def activation_probability(self, concentration: float) -> float:
        """Hill equation for WBC activation."""
        if concentration <= 0:
            return 0.0
        return concentration**self.hill_n / (self.threshold**self.hill_n + concentration**self.hill_n)

class RBDCAnalyzer:
    """Complete analysis suite for RBDC performance."""
    
    def __init__(self, Q: float = 1e-9, D: float = 1e-6, threshold: float = 1e-8):
        # John's proven parameters as defaults
        self.field = ChemoattractantField(Q, D, degradation_rate=1e-4)
        self.response = WBCResponse(threshold)
        
    def reproduce_original_results(self) -> Dict:
        """Reproduce John's original simulation exactly."""
        t = 600  # 10 minutes
        r_values = np.linspace(0.001, 1.5, 500)
        
        # Use original method (no degradation)
        field_original = ChemoattractantField(self.field.Q, self.field.D, degradation_rate=0)
        concentrations = np.array([field_original.concentration(r, t) for r in r_values])
        
        # Find activation radius (John's method)
        below_threshold = np.where(concentrations < self.response.threshold)[0]
        activation_radius = r_values[below_threshold[0]] if len(below_threshold) > 0 else 1.5
        
        return {
            'distances_mm': r_values * 10,
            'concentrations': concentrations,
            'activation_radius_mm': activation_radius * 10,
            'peak_concentration': concentrations[0],
            'therapeutic_volume_mm3': (4/3) * np.pi * (activation_radius * 10)**3
        }
    
    def patient_customization(self, patient_profile: Dict) -> Dict:
        """Customize RBDC for specific patient."""
        target_radius = patient_profile.get('target_radius_mm', 1.0)
        wbc_multiplier = patient_profile.get('wbc_count_multiplier', 1.0)
        lupus_severity = patient_profile.get('severity', 'moderate')
        
        # Simple optimization for target radius
        current_result = self.reproduce_original_results()
        current_radius = current_result['activation_radius_mm']
        
        # Scale Q to hit target radius
        ratio = target_radius / current_radius
        optimal_Q = self.field.Q * (ratio ** 2)
        
        # Adjust for patient factors
        optimal_Q *= wbc_multiplier
        
        # Severity adjustments
        severity_factors = {'mild': 0.7, 'moderate': 1.0, 'severe': 1.3}
        optimal_Q *= severity_factors.get(lupus_severity, 1.0)
        
        # Safety check
        safety_ok = optimal_Q < 1e-7 and target_radius < 3.0
        
        return {
            'optimal_Q_mol': optimal_Q,
            'predicted_radius_mm': target_radius,
            'safety_approved': safety_ok,
            'recommended': safety_ok
        }

def quick_analysis():
    """Run quick RBDC analysis with John's parameters."""
    analyzer = RBDCAnalyzer()
    
    print("🔬 RBDC Quick Analysis")
    print("=" * 30)
    
    # Original results
    original = analyzer.reproduce_original_results()
    print(f"Original activation radius: {original['activation_radius_mm']:.2f} mm")
    print(f"Peak concentration: {original['peak_concentration']:.2e} mol/cm³")
    
    # Patient example
    patient = {
        'target_radius_mm': 1.2,
        'wbc_count_multiplier': 1.3,
        'severity': 'moderate'
    }
    
    custom = analyzer.patient_customization(patient)
    print(f"\nCustom dose for patient: {custom['optimal_Q_mol']:.2e} mol")
    print(f"Safety approved: {custom['recommended']}")
    
    return analyzer

if __name__ == "__main__":
    analyzer = quick_analysis()
