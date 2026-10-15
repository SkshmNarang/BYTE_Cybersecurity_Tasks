# -*- coding: utf-8 -*-
"""
Process and generate professional multi-resolution Windows .ico files
for PixelPry.exe across all 3 generated concepts.
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFilter

ICO_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

def make_squircle_mask(size, radius, padding):
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([padding, padding, size - padding, size - padding], radius=radius, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(1.2))

def create_shield_mask(im):
    # For concept 2: crop shield to remove bottom text 'PIXELPRY' and isolate shield
    w, h = im.size
    # Crop to top 820 pixels to remove text
    shield = im.crop((80, 40, w - 80, 820))
    # Resize to square 1024x1024
    shield = shield.resize((1024, 1024), Image.Resampling.LANCZOS)
    # Mask out outer dark background
    gray = shield.convert('L')
    # Threshold dark background (< 38)
    mask = Image.new('L', (1024, 1024), 255)
    draw = ImageDraw.Draw(mask)
    # Circular/shield boundary
    return shield.convert('RGBA')

def process_concept_1(src_path, out_png, out_ico):
    im = Image.open(src_path).convert('RGBA')
    mask = make_squircle_mask(1024, radius=210, padding=122)
    im.putalpha(mask)
    # Crop to squircle bounds with tiny margin
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
        # Pad slightly to square
        max_dim = max(im.width, im.height)
        sq = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
        sq.paste(im, ((max_dim - im.width)//2, (max_dim - im.height)//2))
        im = sq.resize((512, 512), Image.Resampling.LANCZOS)
    im.save(out_png, 'PNG')
    # Save multi-res ICO
    im.save(out_ico, format='ICO', sizes=ICO_SIZES)
    print(f"[+] Concept 1 processed: {out_png} & {out_ico}")

def process_concept_2(src_path, out_png, out_ico):
    im = Image.open(src_path).convert('RGBA')
    # Crop out the text at bottom and focus on the shield emblem
    w, h = im.size
    shield_box = (120, 80, w - 120, 840)
    im_cropped = im.crop(shield_box)
    max_dim = max(im_cropped.width, im_cropped.height)
    sq = Image.new('RGBA', (max_dim, max_dim), (33, 37, 49, 255))
    sq.paste(im_cropped, ((max_dim - im_cropped.width)//2, (max_dim - im_cropped.height)//2))
    mask = make_squircle_mask(max_dim, radius=int(max_dim*0.2), padding=int(max_dim*0.06))
    sq.putalpha(mask)
    sq = sq.resize((512, 512), Image.Resampling.LANCZOS)
    sq.save(out_png, 'PNG')
    sq.save(out_ico, format='ICO', sizes=ICO_SIZES)
    print(f"[+] Concept 2 processed: {out_png} & {out_ico}")

def process_concept_3(src_path, out_png, out_ico):
    im = Image.open(src_path).convert('RGBA')
    mask = make_squircle_mask(1024, radius=215, padding=98)
    im.putalpha(mask)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
        max_dim = max(im.width, im.height)
        sq = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
        sq.paste(im, ((max_dim - im.width)//2, (max_dim - im.height)//2))
        im = sq.resize((512, 512), Image.Resampling.LANCZOS)
    im.save(out_png, 'PNG')
    im.save(out_ico, format='ICO', sizes=ICO_SIZES)
    print(f"[+] Concept 3 processed: {out_png} & {out_ico}")

def main():
    base_brain = r"C:\Users\Saksham Narang\.gemini\antigravity\brain\5c614c2d-d7dd-4aa0-8bf9-a35dc775876d"
    c1_src = os.path.join(base_brain, "pixelpry_icon_concept_1_lens_1792103388908.jpg")
    c2_src = os.path.join(base_brain, "pixelpry_icon_concept_2_shield_1792103407351.jpg")
    c3_src = os.path.join(base_brain, "pixelpry_icon_concept_3_cube_1792103425567.jpg")

    os.makedirs("assets", exist_ok=True)

    # Process all 3 concepts
    process_concept_1(c1_src, "assets/PixelPry_Concept1_Lens.png", "assets/PixelPry_Concept1_Lens.ico")
    process_concept_2(c2_src, "assets/PixelPry_Concept2_Shield.png", "assets/PixelPry_Concept2_Shield.ico")
    process_concept_3(c3_src, "assets/PixelPry_Concept3_Cube.png", "assets/PixelPry_Concept3_Cube.ico")

    # Set Concept 1 (Forensic Lens prying open pixels) as default PixelPry.ico
    shutil.copy("assets/PixelPry_Concept1_Lens.ico", "PixelPry.ico")
    shutil.copy("assets/PixelPry_Concept1_Lens.ico", "assets/PixelPry.ico")
    print("[+] Updated default PixelPry.ico with Concept 1 (Forensic Lens)!")

if __name__ == "__main__":
    main()
