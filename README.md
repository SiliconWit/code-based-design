# How to Run the Heatsink Designer in FreeCAD

## Prerequisites
1. Install FreeCAD (Version 0.20 or later recommended)
2. Make sure Python is included in your FreeCAD installation (it usually is by default)

## Setting Up the Macro
1. Open FreeCAD
2. Go to **Tools → Macro → Macros...** in the top menu
3. In the Macro dialog:
   - Click "Create"
   - Name your macro (e.g., "heatsink_designer.py", or "heatsink_designer.FCMacro")
   - Click "OK"
4. In the macro editor that opens:
   - Delete any existing code
   - Copy and paste the entire heatsink designer code
   - Click "Save"
   - Close the editor

## Running the Macro
1. Go to **Tools → Macro → Macros...** again
2. Select your heatsink macro from the list
3. Click "Execute"

## Using the Designer
When you run the macro, you'll see a dialog box asking for:
1. **Base Size** (50-200mm):
   - This is the main dimension of your heatsink
   - Default is 100mm
   - Use larger values for bigger heatsinks

2. **Number of Designs** (1-15):
   - Choose how many different designs to generate
   - Maximum is 15 to prevent FreeCAD from crashing
   - Recommended to start with 5-6 designs

3. After clicking "OK", you'll need to:
   - Select a folder where you want to save the results
   - Wait while the designs are generated

## Output Files
The program will create three files in your selected folder:
1. A FreeCAD file (.FCStd) containing all 3D models
2. A CSV file with measurements and performance data
3. A summary report of the designs

## Viewing Results
1. The 3D designs will appear automatically in FreeCAD:
   - Different colors for each design
   - Arranged in a grid layout
   - You can rotate and zoom to inspect them

2. A summary window will show:
   - Number of designs created
   - Pattern types used
   - Average heat dissipation
   - Best performing design

## Tips
- Start with a small number of designs (3-4) for your first try
- The designs are random, so running the macro multiple times will give different results
- You can open the CSV file in Excel to analyze the designs
- Use FreeCAD's measurement tools to inspect the 3D models

## Troubleshooting
- If FreeCAD becomes slow: Try generating fewer designs
- If designs look too small/large: Adjust the base size
- If the program crashes: Restart FreeCAD and try with fewer designs

## Notes
- Each design will be randomly generated with different:
  - Fin patterns (straight, angled, or zigzag)
  - Dimensions
  - Colors
- The program calculates:
  - Heat dissipation
  - Weight
  - Surface area
  - Manufacturing complexity
