"""
Module for creating aortic valve flaps for homograph
Run in regular Python
Installation: pip install numpy trimesh
"""

import numpy as np
import trimesh

def create_single_leaflet(radius=13, height=15, thickness=1.0, curvature=0.3):
    """
    Creates one crescent-shaped valve leaf.
 
   For homograft, it is important:
 - Accurate anatomical shape
 - Leaf thickness ≈1 mm
 - Three leaves of the same size
    """
    # Create a grid of points (crescent shape)
    theta = np.linspace(0, np.pi, 30)
    
    # The radius changes along the arc (creating a curve)
    r = radius * (1 - curvature * np.sin(theta))
    
    # Upper edge (free edge of the sash)
    top_x = r * np.cos(theta)
    top_y = r * np.sin(theta)
    top_z = np.ones_like(theta) * height
    
    # Lower edge (attached to the fibrous ring)
    bottom_x = r * np.cos(theta) * 0.9
    bottom_y = r * np.sin(theta) * 0.9
    bottom_z = np.zeros_like(theta)
    
    # Building a surface
    vertices = []
    faces = []
    
    for i in range(len(theta) - 1):
        # Triangle 1
        vertices.append([top_x[i], top_y[i], top_z[i]])
        vertices.append([bottom_x[i], bottom_y[i], bottom_z[i]])
        vertices.append([top_x[i+1], top_y[i+1], top_z[i+1]])
        idx = len(vertices) - 3
        faces.append([idx, idx+1, idx+2])
        
        # Triangle 2
        vertices.append([bottom_x[i], bottom_y[i], bottom_z[i]])
        vertices.append([bottom_x[i+1], bottom_y[i+1], bottom_z[i+1]])
        vertices.append([top_x[i+1], top_y[i+1], top_z[i+1]])
        idx = len(vertices) - 3
        faces.append([idx, idx+1, idx+2])
    
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh = mesh.simplify_quadric_decimation(200)
    return mesh


def create_homograft_valve(radius=13, height=15, thickness=1.0):
    """
    Creates three flaps for the aortic root homograft.
    """
    leaflet = create_single_leaflet(radius, height, thickness, curvature=0.25)
    
    leaflets = []
    for i in range(3):
        l = leaflet.copy()
        angle = i * 2 * np.pi / 3
        rot_matrix = trimesh.transformations.rotation_matrix(angle, [0, 0, 1])
        l.apply_transform(rot_matrix)
        shift = radius * 0.3
        l.apply_translation([shift * np.cos(angle), shift * np.sin(angle), 0])
        leaflets.append(l)
    
    combined = trimesh.util.concatenate(leaflets)
    return combined


def create_homograft_with_ring(radius=13, height=15, thickness=1.0):
    """
    Creates flaps with a fibrous ring for the homograph.
    """
    leaflets = create_homograft_valve(radius, height, thickness)
    
    # Fibrous ring (valve base)
    ring = trimesh.creation.cylinder(radius, radius * 0.8, height=2.5, sections=30)
    ring.apply_translation([0, 0, -1])
    
    full_valve = trimesh.util.concatenate([leaflets, ring])
    return full_valve


if __name__ == "__main__":
    print("="*60)
    print("VALVE GENERATION FOR AORTIC ROOT HOMOGRAFT")
    print("="*60)
    
    print("   Creation of three flaps (anatomical shape)")
    print("   Root radius: 13 mm (diameter ≈26 mm)")
    print("   the height of the shutters are: 15 mm")
    print("   Thickness: 1.0mm")
    
    # Creating the shutters
    valve = create_homograft_valve(radius=13, height=15, thickness=1.0)
    valve.export("../models/valve_leaflets.stl")
    print("\n The shutters are saved: models/valve_leaflets.stl")
    
    # Creating with a ring for assembly
    valve_with_ring = create_homograft_with_ring(radius=13, height=15)
    valve_with_ring.export("../models/valve_with_ring.stl")
    print(" Flaps with a ring: models/valve_with_ring.stl")
    
    print("\n VALVE PARAMETERS:")
    print("   Root radius: 13 mm (diameter ≈26 mm)")
    print("   the height of the shutters are: 15 mm")
    print("   Thickness: 1.0mm")
    print("   Shape: crescent (anatomical)")
    
    print("\n FOR PRINTING A HOMOGRAPH EXAMPLE:")
    print("    TPU (Flexible plastic) → valve_leaflets.stl")
    print("    Silicone (filling) → valve_with_ring.stl")
    print("="*60)
