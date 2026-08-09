# tools/pdf/pdf_generator.py

from fpdf import FPDF
from typing import Dict

def generate_pdf_file(cert_data: Dict[str, str], output_path: str):
    """
    Generates a PDF certificate and saves it to the specified file path.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, txt='Certificate of Data Wipe', ln=1, align='C')
    pdf.ln(10)

    for key, value in cert_data.items():
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(w=0, h=8, txt=f"{key.replace('_', ' ').title()}:", ln=1)
        pdf.set_font('Helvetica', '', 12)
        pdf.multi_cell(w=0, h=6, txt=value, align='L')
        pdf.ln(4)

    pdf.output(output_path)