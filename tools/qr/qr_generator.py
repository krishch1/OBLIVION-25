# tools/qr/qr_generator.py

import qrcode

def generate_qr_code_file(data: str, output_path: str):
    """
    Generates a QR code and saves it to the specified file path.
    """
    qr_img = qrcode.make(data)
    qr_img.save(output_path)