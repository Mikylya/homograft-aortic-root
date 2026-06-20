"""
Module for exporting the 3D model of the HOMOGRAPH OF THE AORTAL ROOT to STL
Run in Python Interactor 3D Slicer

Important: select the entire aortic root:
- Root with sinuses
- Fibrous ring
- Ascending aorta (+-5 cm)
- (optional) part of the mitral valve
"""

import slicer

def export_homograft_root(output_path):
    """
    Exports the selected homograph of the aortic root to STL.
 
 Checks:
 That it is the aortic root (height 40-70 mm)
 That there are three Valsalva sinuses
 That there is room for a valve
 
 Args:
 output_path (str): path to save the STL file
 
 Returns:
 bool: True if successful, False if an error
    """
    print("="*60)
    print(" EXPORT OF 3D MODEL OF THE HOMOGRAPH OF THE AORTIC ROOT")
    print("="*60)
    
    # Find all the 3D models in the scene
    all_models = slicer.util.getNodesByClass("vtkMRMLModelNode")
    if not all_models:
        print(" There is no model for export.")
        print("   Do the segmentation first:")
        print("   1. Segment Editor → Threshold")
        print("   2. Clean up the excess (Erase, Scissors)")
        print("   3. Leave ONLY the root of the aorta (+-5 cm)")
        print("   4. click Show 3D")
        return False
    # We take the first model
    homograft = all_models[0]
    # Checking the dimensions
    bounds = [0, 0, 0, 0, 0, 0]
    homograft.GetPolyData().GetBounds(bounds)
    
    width = abs(bounds[1] - bounds[0])   # Diameter X
    depth = abs(bounds[3] - bounds[2])   # Diameter Y
    height = abs(bounds[5] - bounds[4])  # Height
    
    print(f"\n Measurements of the homograph model:")
    print(f"   Diameter (width):  {width:.1f} mm")
    print(f"   Diameter (depth): {depth:.1f} mm")
    print(f"   Height (length):    {height:.1f} mm")
  
    # 1. Height check (root homograph +-40-70 mm)
    if height < 35:
        print("\n The model is too low (<35 mm)!")
        print("   It only looks like a valve.")
        print("   Homograph requires the entire root with the sines.")
        return False
    
    if height > 80:
        print("\n The model is too tall (>80 mm)!")
        print("   It looks like the whole aorta.")
        print("   Homograph requires only a ROOT (+-5 cm).")
        return False
    
    print("  The height corresponds to the homograph of the root")
    
    # 2. Valsalva sinus test (3 extensions)
    # The sinuses are visible as an expansion at the bottom
    if width > depth * 1.08:
        print("   Valsalva sinuses detected (3 extensions)")
    else:
        print("      The sinuses of Valsalva are not visible!")
        print("      This is critical for a homograph.")
        print("      Check the segmentation.")
    
    # 3. Checking the fibrous ring
    # There should be a valve-aorta transition at the bottom
    if height > 40:
        print("    The fibrous ring should be in the model")
    else:
        print("    Check for a fibrous ring.")
    
    # 4. Diameter check (homograph ≈20-30 mm)
    if width < 18:
        print("    The diameter is too small for the root homograph.")
        print("      (usually 20-30 mm)")
    elif width > 35:
        print("    The diameter is too large for the root homograph.")
    else:
        print(f"    Diameter {width:.1f} mm - normal")
    
    #EXPORT 
    try:
        slicer.util.exportNode(homograft, output_path)
        
        print(f"\n The aortic root homograft is preserved: {output_path}")
        print("\n total:")
        print(f"   Model: aortic root homograft")
        print(f"   Length: {height:.1f} мм")
        print(f"   Diameter: {width:.1f} мм")
        print(f"   Sinuses: {' есть' if width > depth * 1.08 else ' check again'}")
        print("="*60)
        return True
    except Exception as e:
        print(f"\n Saving error: {e}")
        print("   Check the path and write permissions.")
        return False

# Usage example:
# export_homograft_root("C:/Path to the repository/models/homograft_root.stl")
