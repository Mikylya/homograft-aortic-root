# 3D-Printed Homograft Aortic Root Model

Author: Mikulyak Sofya  
Goal: MIT/Peking / Tsinghua Admissions — Science and Technology Portfolio  
Repository: (https://github.com/Mikylya/homograft-aortic-root)


# Overview

This project creates a **complete, patient-specific 3D model of an aortic root homograft** — an anatomically accurate replica of the human aortic root with all structures:

- Aortic root with **3 sinuses of Valsalva**
- **Functional aortic valve** (3 leaflets that open/close under pressure)
- **Fibrous ring** (base for leaflet attachment)
- **Ascending aorta** (≈5 cm above the root)

  **The model is designed for surgical planning, training, and hemodynamic testing.**
  
  # What is an Aortic Root Homograft?

A **homograft** is a human donor aortic root used for transplantation. Unlike mechanical valves or synthetic grafts:

 Feature | Homograft 
 **Source** | Human donor 
 **Structure** | Complete root: valve + sinuses + ascending aorta 
 **Advantage** | No lifelong anticoagulation needed 
 **Use** | Root replacement, especially in young patients and infections 

**This project creates a 3D model of a homograft for surgical planning.**


# Anatomical Structures Included
Ascending Aorta (≈5 cm) 
Sinuses of Valsalva (3 bulges) 
Aortic Valve (3 leaflets)
Fibrous Ring
Aortic Root (base)

## Pipeline Overview
 CT/MRI DICOM | Segmentation │ STL Export │ 3D Printing 
 (raw data) | (3D Slicer)  │ (Python) │  (SLA / FDM) 
| |
 v

 Manual Cleanup │ Valve Leaflets 
(15-20 min) │ (TPU / Silicone) 

##  Materials

 Component | Material | Why 
 Aortic root (with sinuses) | **Transparent SLA resin** | See internal structures, high detail 
 Valve leaflets | **TPU (NinjaFlex) or Ecoflex 00-30 silicone** | Flexible, opens/closes under pressure 
 Fibrous ring | Integrated in the root | Provides attachment for leaflets 
 Assembly | **Medical-grade adhesive** | Secure attachment 

## Repository Structure
homograft-aortic-root/
| README.md # This file
|LICENSE # MIT License
| requirements.txt # Python dependencies
codes/
│- 01_load_dicom.py # DICOM loader (3D Slicer)
│-02_export_homograft.py # Export homograft root (3D Slicer)
│- 03_create_valve.py # Generate valve leaflets
│- 04_test_homograft.py # Test valve function
| models/
│-homograft_root.stl # The 3D printable model
| images/
│-printed_model.jpg # Photos of the printed model
| docs/
|= project_report.pdf # Full project report

##  How to Run
### Prerequisites
1. **3D Slicer** ((https://www.slicer.org/))
2. **Python 3.8+** with:
   ```bash
   pip install -r requirements.txt
Step 1: Load CT Data
python
# In 3D Slicer Python Interactor (View → Python Interactor)
exec(open("codes/01_load_dicom.py").read())
volume = load_dicom("path/to/your/dicom/folder")
Step 2: Segment the Aortic Root
Open Segment Editor
Threshold: 150–300 HU → Apply
Clean up: Use Erase, Scissors, Paint
Keep ONLY the aortic root (≈5 cm with sinuses)
Click Show 3D
Step 3: Export STL
python
exec(open("codes/02_export_homograft.py").read())
export_homograft_root("models/homograft_root.stl")
The code will:
Check that you have the aortic root (not the whole aorta)
Check for sinuses of Valsalva
Confirm dimensions
Step 4: Generate Valve Leaflets
bash
python codes/03_create_valve.py
Step 5: Print
Component	Printer	Settings
Aortic root	SLA	0.05 mm layer, transparent resin
Valve leaflets	FDM (TPU)	0.1 mm layer, slow speed (20 mm/s)
Step 6: Assemble
Insert leaflets into the aortic root
Secure at the fibrous ring
Test under water flow
Step 7: Test Valve Function
bash
python codes/04_test_homograft.py
 Results
Quantitative Measurements
Parameter	Value
Aorta height	40–70 mm (patient-specific)
Aorta diameter	20–30 mm
Leaflet height	15 mm
Leaflet thickness	1.0 mm
Opening pressure	80 mmHg
Closing pressure	120 mmHg
Valve Function Test
The valve successfully opens under forward flow and closes under backflow, mimicking native valve mechanics.
[IMAGE] (now i haven`t got it)

 **Why This Project for MIT / Tsinghua**
This project demonstrates applied physics, mathematics, and engineering:

Domain	Skills Applied
Mathematics	Computational geometry, 3D transformations
Physics	Fluid dynamics, pressure gradients
Computer Science	Medical image processing, Python algorithms
Engineering	Additive manufacturing, biomaterials
The medical application is a use case - the core skills are physics and computation.

 Future Work
Goal	Method	Timeline
Multi-material printing	PolyJet (rigid + flexible in one print)	Short-term
AI segmentation	nnU-Net integration	Short-term
Clinical validation	Study with surgical residents	Medium-term
Pressure sensors	Embedded IoT sensors	Long-term
! Limitations
Single-material printing: The model uses separate materials; ideal is multi-material in one print

Leaflet durability: TPU leaflets may fatigue after repeated cycling

No pulsatile flow: Current test uses steady pressure; future: pulse duplicator

**License**
MIT License - free for academic and research use.

 **Contact**
Author: Mikulyak Sofya
Email: micksof@ya.ru
GitHub: (https://github.com/Mikylya/homograft-aortic-root)
LinkedIn: https://github.com/Mikylya

 *Acknowledgments*
3D Slicer community for open-source medical imaging tools

MIT /Peking/ Tsinghua admissions for inspiring this work
