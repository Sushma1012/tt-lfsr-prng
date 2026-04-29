import klayout.db as db

GDS = "tt_submission/tt_um_sushma1012_lfsr_prng.gds"
CORRECT_Y1 = 110520
CORRECT_Y2 = 111520

layout = db.Layout()
layout.read(GDS)

fixed = 0
for layer_idx in layout.layer_indices():
    info = layout.get_info(layer_idx)
    if info.layer != 71 or info.datatype != 20:
        continue
    for cell in layout.each_cell():
        for shape in cell.shapes(layer_idx).each():
            bbox = shape.bbox()
            if bbox.top == CORRECT_Y2 and bbox.bottom != CORRECT_Y1:
                # Replace polygon with corrected box
                new_box = db.Box(bbox.left, CORRECT_Y1, bbox.right, CORRECT_Y2)
                shape.polygon = db.Polygon(new_box)
                fixed += 1
                print(f"  Fixed: ({bbox.left},{bbox.bottom},{bbox.right},{bbox.top}) -> y1={CORRECT_Y1}")

print(f"\nTotal fixed: {fixed}")
layout.write(GDS)
print("GDS written.")
