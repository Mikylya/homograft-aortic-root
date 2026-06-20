"""
Module for loading DICOM data of a donor's aorta into 3D Slicer
 Run in Python Interactor 3D Slicer!!
"""

import slicer

def load_dicom(folder_path):
    """
    Loads DICOM from a folder and checks the data quality.
 
 Args:
 folder_path (str): path to the folder with DICOM files
 
 Returns:
 volume_node: node with the loaded tomography
    """
    print("="*60)
    print("DOWNLOADING DICOM-DATA FROM THE DONOR AORTA")
    print("="*60)
    print(f"   Folder: {folder_path}")
    
    # Uploading data
    loaded_nodes = slicer.util.loadDICOM(folder_path)
    
    # find the tomography
    volume_node = None
    for node in loaded_nodes:
        if node.IsA("vtkMRMLScalarVolumeNode"):
            volume_node = node
            break
    
    if not volume_node:
        print(" Tomography was not found!")
        return None
    
    # check the quality
    spacing = volume_node.GetSpacing()
    slice_thickness = spacing[2]
    
    print(f"\n Uploaded: {volume_node.GetName()}")
    print(f"Slice thickness: {slice_thickness:.2f} мм")
    
    if slice_thickness > 1.0:
        print(" WARNING: the slices are thicker than 1 mm!")
        print("  Homograft requires slices ≤ 1 mm.")
        print("   The model may be inaccurate.")
    else:
        print("The quality is excellent. You can build a homograph model.")
    
    print("="*60)
    return volume_node

# Usage example:
# volume = load_dicom("C:/path_to_DICOM_donor")
