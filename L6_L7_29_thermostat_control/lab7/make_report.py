"""Run after saving the four screenshots in evidence/ as named below."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

root = Path(__file__).resolve().parent
items = [('1_original.png', 'Original application: invalid input'),
         ('2_fuzz_fail.png', 'Hypothesis tests against original application'),
         ('3_fixed.png', 'Fixed application: invalid inputs handled'),
         ('4_fuzz_pass.png', 'Hypothesis tests against fixed application')]
for name, _ in items:
    if not (root / 'evidence' / name).is_file():
        raise SystemExit(f'Missing screenshot: evidence/{name}')
c = canvas.Canvas(str(root / 'Lab7_FuzzTesting_Report.pdf'), pagesize=A4)
w, h = A4
for i, (name, title) in enumerate(items, 1):
    c.setFont('Helvetica-Bold', 17)
    c.drawString(40, h-48, 'Lab 7 | Thermostat Control | 29')
    c.setFont('Helvetica', 12)
    c.drawString(40, h-78, title)
    img = ImageReader(str(root / 'evidence' / name))
    iw, ih = img.getSize()
    scale = min((w-80)/iw, (h-180)/ih)
    c.drawImage(img, 40, h-110-ih*scale, iw*scale, ih*scale)
    c.drawString(40, 35, f'Evidence {i} of 4')
    c.showPage()
c.save()
