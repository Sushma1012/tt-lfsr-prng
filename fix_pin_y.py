import re, shutil, pathlib

DEF_FILE = pathlib.Path("runs/wokwi/final/def/tt_um_sushma1012_lfsr_prng.def")
BACKUP = DEF_FILE.with_suffix(".def.bak")

CORRECT_Y1 = "110.520"

rect_re = re.compile(
    r'(\bRECT\s+[\d.]+\s+)([\d.]+)(\s+[\d.]+\s+)(111\.520\b)'
)

shutil.copy(DEF_FILE, BACKUP)
text = DEF_FILE.read_text()

fixed, n = rect_re.subn(
    lambda m: f"{m.group(1)}{CORRECT_Y1}{m.group(3)}{m.group(4)}", text
)

DEF_FILE.write_text(fixed)
print(f"Fixed {n} RECT entries  (backup -> {BACKUP})")
