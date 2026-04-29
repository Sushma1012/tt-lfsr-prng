import klayout.db as db

GDS_IN  = "tt_submission/tt_um_sushma1012_lfsr_prng.gds"
GDS_OUT = "tt_submission/tt_um_sushma1012_lfsr_prng.gds"

layout = db.Layout()
layout.read(GDS_IN)

# TT pin label layer in sky130A is met4 drawing = layer 71/20
# Pin text/label correct y1 = 110.52 um, y2 = 111.52 um
# In GDS units (1nm = 1 unit if dbu=0.001)
dbu = layout.dbu
print(f"DBU: {dbu}")

CORRECT_Y1 = 110520  # 110.520 um in nm
CORRECT_Y2 = 111520  # 111.520 um in nm

fixed = 0
for layer_idx in layout.layer_indices():
    info = layout.get_info(layer_idx)
    for cell in layout.each_cell():
        for shape in cell.shapes(layer_idx).each():
            if shape.is_box():
                box = shape.box
                # Check if this is a top-edge pin (y2 == 111520 but y1 wrong)
                if box.top == CORRECT_Y2 and box.bottom != CORRECT_Y1:
                    new_box = db.Box(box.left, CORRECT_Y1, box.right, CORRECT_Y2)
                    shape.box = new_box
                    fixed += 1

print(f"Fixed {fixed} shapes in GDS")
layout.write(GDS_OUT)
print("Done.")
