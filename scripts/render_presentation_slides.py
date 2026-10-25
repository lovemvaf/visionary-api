import os
import fitz  # PyMuPDF

pdf_path = "deliverables/VISIONARY_TH71108_FINAL_PRESENTATION.pdf"
output_dir = "deliverables/slide-previews"
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total slides in presentation: {len(doc)}")

for page_num in range(len(doc)):
    page = doc[page_num]
    pix = page.get_pixmap(dpi=150)
    out_file = os.path.join(output_dir, f"slide_{page_num + 1:02d}.png")
    pix.save(out_file)
    print(f"Rendered: {out_file} ({pix.width}x{pix.height})")

print("All slides rendered successfully.")
