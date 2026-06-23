"""
Module for testing the homograft of the aortic root
Run in regular Python
Installation: pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

def test_homograft_function(cycles=5, beats_per_minute=70):
    """
    Tests the functionality of the aortic root homograft.
    """
    print("="*60)
    print(" TESTING OF THE AORTIC ROOT HOMOGRAFT")
    print("="*60)
    
    cycle_time = 60 / beats_per_minute
    dt = 0.01
    total_time = cycles * cycle_time
    time = np.arange(0, total_time, dt)
    
    # Pressure in the left ventricle and aorta
    lv_pressure = 80 + 40 * np.sin(2 * np.pi * time / cycle_time) ** 2
    aortic_pressure = 80 + 20 * np.sin(2 * np.pi * time / cycle_time)
    
    # The valve is open at systole
    valve_open = lv_pressure > aortic_pressure
    
    # Hemodynamic parameters of homograft
    transvalvular_gradient = lv_pressure - aortic_pressure
    effective_orifice_area = 2.0 + 0.5 * valve_open  # mm2 (simplified)
    
    # Chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    
    # Chart 1: Pressure
    ax1.plot(time, lv_pressure, label='Left Ventricle', color='blue', linewidth=2)
    ax1.plot(time, aortic_pressure, label='Aorta', color='red', linewidth=2)
    ax1.set_ylabel('Pressure (mmHg)')
    ax1.set_title('Гемодинамика гомографта корня аорты')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Chart 2:Valve opening
    ax2.plot(time, valve_open, label='Valve Open', color='green', linewidth=2)
    ax2.set_ylabel('Valve Status')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_title('Operation of the homograph valve')
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Closed', 'Open'])
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../images/homograft_test.png', dpi=150)
    plt.show()
    
    # RESULTS
    open_time = np.sum(valve_open) * dt
    closed_time = np.sum(~valve_open) * dt
    
      print("\n TEST RESULTS:")
    print(f"   Cycles: {cycles}")
      print(f"   Frequency: {beats_per_minute} beats/minutes")
    print(f"   Opening time: {open_time / cycles:.2f} seconds")
    print(f"   Closing time: {closed_time / cycles:.2f} seconds")
    print(f"   The time share is open: {open_time / total_time * 100:.1f}%")
    print(f"   Maximum gradient: {max(transvalvular_gradient):.1f} mmHg")
    print(f"   Effective hole area: {max(effective_orifice_area):.1f} mm²")
    
    print("\n The aortic root homograft is functional")
    print("="*60)
    return valve_open

if __name__ == "__main__":
    test_homograft_function(cycles=5, beats_per_minute=70)
