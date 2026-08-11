"""
Generate certificates for all 4 students
Course: SOC Analyst - Level 1
Date: 5th October 2025
"""
from PIL import Image, ImageDraw, ImageFont
import os
import qrcode

# Student data
students = [
    {"name": "RAKESH JIMMIDI", "cert_id": "INFOD-SOC-2025-001"},
    {"name": "DASARI TEJESH", "cert_id": "INFOD-SOC-2025-002"},
    {"name": "KOSURI MAMATHA VALLI", "cert_id": "INFOD-SOC-2025-003"},
    {"name": "YEDLA TEJOMAYA", "cert_id": "INFOD-SOC-2025-004"},
]

TEMPLATE_PATH = "certs/live_training_tempjpg.jpeg"
OUTPUT_DIR = "dumpfolder/certificates"
ISSUE_DATE = "5th October 2025"
VERIFY_URL = "https://www.infosecdairies.io/Verify"

# Colors
COLOR_OLIVE = (193, 200, 135)  # #C1C887 — date & cert-id
COLOR_GREEN = (97, 255, 120)   # green — student name

def generate_certificate(student_name, cert_id, output_path):
    # Load template
    template = Image.open(TEMPLATE_PATH)
    width, height = template.size
    
    draw = ImageDraw.Draw(template)
    
    # Fonts
    try:
        font_name = ImageFont.truetype("C:/Windows/Fonts/timesbd.ttf", int(height * 0.065))
        font_details = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", int(height * 0.022))
    except:
        font_name = ImageFont.load_default()
        font_details = ImageFont.load_default()
    
    # ── 1. STUDENT NAME ──────────────────────────────────────────────────────────
    name_y = int(height * 0.265)
    bbox = draw.textbbox((0, 0), student_name, font=font_name)
    text_w = bbox[2] - bbox[0]
    name_x = (width - text_w) // 2 - int(width * 0.10)
    draw.text((name_x, name_y), student_name, fill=COLOR_GREEN, font=font_name)
    
    # ── 2. DATE OF ISSUE ─────────────────────────────────────────────────────────
    date_x = int(width * 0.150)
    date_y = int(height * 0.772)
    draw.text((date_x, date_y), ISSUE_DATE, fill=COLOR_OLIVE, font=font_details)
    
    # ── 3. CERTIFICATION ID ───────────────────────────────────────────────────────
    cert_x = int(width * 0.350)
    cert_y = int(height * 0.772)
    draw.text((cert_x, cert_y), cert_id, fill=COLOR_OLIVE, font=font_details)
    
    # ── 4. QR CODE ──────────────────────────────────────────────────────────────
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(VERIFY_URL)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_size = int(width * 0.12)
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    qr_x = int(width * 0.82)
    qr_y = int(height * 0.75)
    
    template.paste(qr_img, (qr_x, qr_y))
    
    # Save
    template.save(output_path)
    print(f"✅ Generated: {output_path}")

# Generate all certificates
os.makedirs(OUTPUT_DIR, exist_ok=True)

for student in students:
    safe_name = student["name"].replace(" ", "_").lower()
    output_path = os.path.join(OUTPUT_DIR, f"certificate_{safe_name}.png")
    generate_certificate(student["name"], student["cert_id"], output_path)

print("\n" + "="*60)
print("All certificates generated successfully!")
print("="*60)
for student in students:
    print(f"   {student['name']}: {student['cert_id']}")
print(f"   QR Code links to: {VERIFY_URL}")
