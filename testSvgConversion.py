# wand_test.py — WORKS ON M2 MAC WITH HOMEBREW IMAGEMAGICK
import os
from wand.image import Image
from pathlib import Path

# ONLY NEEDED ON M2 MAC WITH HOMEBREW + CONDA
os.environ["MAGICK_HOME"] = "/opt/homebrew"
if "DYLD_LIBRARY_PATH" in os.environ:
    os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/lib:" + os.environ["DYLD_LIBRARY_PATH"]
else:
    os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/lib"

def convert_svg_to_png(svg_path: str, png_path: str = "wand_output.png"):
    with Image(filename=svg_path, format='svg') as img:
        img.format = 'png'
        img.save(filename=png_path)
    print(f"SUCCESS! PNG saved: {png_path}")

# Test it
convert_svg_to_png("matthew_mikos_birth_chart.svg", "matthew_mikos_birth_chart.png")