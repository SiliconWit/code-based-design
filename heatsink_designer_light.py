import FreeCAD as App
import Part
import math
import csv
import os
import random
from datetime import datetime
from PySide import QtGui
from FreeCAD import Base

def create_heatsink(params):
    """Creates a heatsink with given parameters"""
    # Create base plate
    base = Part.makeBox(params['width'], params['length'], params['base_height'])
    
    # Add fins based on pattern
    fins = []
    if params['pattern'] == 'straight':
        spacing = (params['width'] - params['fin_thickness']) / (params['num_fins'] - 1)
        for i in range(params['num_fins']):
            x_pos = i * spacing
            fin = Part.makeBox(params['fin_thickness'], 
                             params['length'], 
                             params['fin_height'])
            fin.translate(Base.Vector(x_pos, 0, params['base_height']))
            fins.append(fin)
            
    elif params['pattern'] == 'angled':
        spacing = (params['width'] - params['fin_thickness']) / (params['num_fins'] - 1)
        for i in range(params['num_fins']):
            x_pos = i * spacing
            fin = Part.makeBox(params['fin_thickness'], 
                             params['length'], 
                             params['fin_height'])
            # Rotate fin
            fin.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), params['fin_angle'])
            fin.translate(Base.Vector(x_pos, 0, params['base_height']))
            fins.append(fin)
            
    elif params['pattern'] == 'zigzag':
        spacing = (params['width'] - params['fin_thickness']) / (params['num_fins'] - 1)
        for i in range(params['num_fins']):
            x_pos = i * spacing
            fin = Part.makeBox(params['fin_thickness'], 
                             params['length'], 
                             params['fin_height'])
            # Alternate fin angles
            angle = params['fin_angle'] if i % 2 == 0 else -params['fin_angle']
            fin.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), angle)
            fin.translate(Base.Vector(x_pos, 0, params['base_height']))
            fins.append(fin)
    
    # Combine base and fins
    heatsink = base
    for fin in fins:
        heatsink = heatsink.fuse(fin)
    
    return heatsink

def analyze_heatsink(shape, params):
    """Calculate basic metrics for the heatsink"""
    # Basic measurements
    volume = shape.Volume / 1000  # cm³
    surface_area = shape.Area / 100  # cm²
    
    # Weight (aluminum)
    density = 2.7  # g/cm³
    weight = volume * density / 1000  # kg
    
    # Basic thermal calculation (simplified)
    h = 10  # Heat transfer coefficient (W/m²K)
    delta_t = 50  # Temperature difference (K)
    heat_dissipation = h * (surface_area/100) * delta_t  # Watts
    
    # Estimate manufacturing complexity
    complexity = params['num_fins'] * 2
    if params['pattern'] in ['angled', 'zigzag']:
        complexity += 10
    
    return {
        'volume_cm3': round(volume, 2),
        'surface_area_cm2': round(surface_area, 2),
        'weight_kg': round(weight, 3),
        'heat_dissipation_W': round(heat_dissipation, 1),
        'complexity_score': complexity
    }

def generate_random_design(base_size):
    """Generate a random heatsink design within practical constraints"""
    patterns = ['straight', 'angled', 'zigzag']
    
    # Random parameters with engineering constraints
    design = {
        'width': random.uniform(base_size * 0.8, base_size * 1.2),
        'length': random.uniform(base_size * 0.8, base_size * 1.2),
        'base_height': random.uniform(5, 15),
        'fin_height': random.uniform(20, 50),
        'fin_thickness': random.uniform(1.5, 3),
        'num_fins': random.randint(5, 15),
        'pattern': random.choice(patterns),
        'fin_angle': random.uniform(10, 30) if random.random() > 0.5 else 0
    }
    
    # Ensure minimum spacing between fins
    min_spacing = 5  # mm
    max_fins = int((design['width'] - min_spacing) / (design['fin_thickness'] + min_spacing))
    design['num_fins'] = min(design['num_fins'], max_fins)
    
    return design

def run_heatsink_study():
    """Main function to run the heatsink design study"""
    # Create dialog for parameters
    dialog = QtGui.QDialog()
    dialog.setWindowTitle("Heatsink Designer")
    layout = QtGui.QVBoxLayout()
    
    # Add input fields
    form_layout = QtGui.QFormLayout()
    
    # Base size input
    base_size_spin = QtGui.QSpinBox()
    base_size_spin.setRange(50, 200)
    base_size_spin.setValue(100)
    base_size_spin.setSuffix(" mm")
    form_layout.addRow("Base Size:", base_size_spin)
    
    # Number of designs input
    num_designs_spin = QtGui.QSpinBox()
    num_designs_spin.setRange(1, 15)  # Limited to prevent crashes
    num_designs_spin.setValue(5)
    form_layout.addRow("Number of Designs (max 15):", num_designs_spin)
    
    layout.addLayout(form_layout)
    
    # Add buttons
    button_box = QtGui.QDialogButtonBox(
        QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)
    layout.addWidget(button_box)
    
    dialog.setLayout(layout)
    
    # Show dialog
    if not dialog.exec_():
        App.Console.PrintMessage("Study cancelled.\n")
        return
    
    # Get parameters
    base_size = base_size_spin.value()
    num_designs = num_designs_spin.value()
    
    # Get output directory
    output_dir = QtGui.QFileDialog.getExistingDirectory(
        None, "Select Output Directory")
    
    if not output_dir:
        App.Console.PrintMessage("No output directory selected.\n")
        return
    
    # Create new document
    doc = App.newDocument("HeatsinkStudy")
    
    # Generate and create designs
    results = []
    max_spacing = base_size * 1.5  # Space between designs
    
    for i in range(num_designs):
        App.Console.PrintMessage(f"\nCreating Design {i+1}...\n")
        
        # Generate random design
        params = generate_random_design(base_size)
        params['name'] = f'Design_{i+1}'
        
        # Create heatsink
        try:
            heatsink = create_heatsink(params)
            
            # Add to document
            obj = doc.addObject("Part::Feature", f"Heatsink_{i+1}")
            obj.Shape = heatsink
            
            # Position each design in a grid (3 columns max)
            row = i // 3
            col = i % 3
            obj.Placement.Base = App.Vector(
                col * max_spacing,
                row * max_spacing,
                0
            )
            
            # Add random color
            obj.ViewObject.ShapeColor = (
                random.random(),
                random.random(),
                random.random()
            )
            
            # Analyze design
            metrics = analyze_heatsink(heatsink, params)
            results.append({**params, **metrics})
            
        except Exception as e:
            App.Console.PrintError(f"Error creating design {i+1}: {str(e)}\n")
            continue
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"heatsink_results_{timestamp}.csv")
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    # Update view
    doc.recompute()
    
    # Set view
    Gui.activeDocument().activeView().viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
    
    # Save FreeCAD document
    fcstd_file = os.path.join(output_dir, f"heatsink_designs_{timestamp}.FCStd")
    doc.saveAs(fcstd_file)
    
    # Show completion message with design summary
    msg = QtGui.QMessageBox()
    msg.setWindowTitle("Study Complete")
    
    # Calculate some statistics
    avg_dissipation = sum(r['heat_dissipation_W'] for r in results) / len(results)
    best_design = max(results, key=lambda x: x['heat_dissipation_W'])
    
    summary = (
        f"Created {len(results)} unique heatsink designs!\n\n"
        f"Design Patterns Used:\n"
        f"- {sum(1 for r in results if r['pattern']=='straight')} Straight\n"
        f"- {sum(1 for r in results if r['pattern']=='angled')} Angled\n"
        f"- {sum(1 for r in results if r['pattern']=='zigzag')} Zigzag\n\n"
        f"Average Heat Dissipation: {avg_dissipation:.1f}W\n"
        f"Best Design: {best_design['name']} ({best_design['heat_dissipation_W']:.1f}W)\n\n"
        f"Results saved to:\n{output_dir}"
    )
    
    msg.setText(summary)
    msg.exec_()

# Run the study when macro is executed
run_heatsink_study()

