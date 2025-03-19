from flask import Flask, request, send_file, render_template
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

current_date = datetime.now().strftime("%d %b %Y")

sign_text = f"""
Signature:                                                                      Date: {datetime.now():%d %b %Y}"""

app = Flask(__name__)


# Function to add text box to PDF
def add_text_box_to_pdf(input_pdf_path, output_pdf_path, vertical, horizontal, color, text):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        # Convert hex color to RGB
        color_rgb = tuple(int(color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        can.setStrokeColorRGB(*color_rgb)  # Set color
        can.setFillColorRGB(*color_rgb)  # Set color
        can.setLineWidth(1)
        can.setFont('Helvetica', 8)  # Modern sans-serif font at smaller size
        # A4 is 595.2 x 841.8 points (1 point = 1/72 inch)
        # 5mm = ~14.17 points
        box_width = 300
        box_height = 120

        # Calculate x position
        if horizontal == 'left':
            x = 14.17  # 5mm from left
        elif horizontal == 'middle':
            x = (595.2 - box_width) / 2
        else:  # right
            x = 595.2 - 14.17 - box_width  # Right edge minus 5mm margin minus width

        # Calculate y position
        if vertical == 'top':
            y = 841.8 - 14.17 - box_height  # Top edge minus 5mm margin minus height
        elif vertical == 'middle':
            y = (841.8 - box_height) / 2
        else:  # bottom
            y = 14.17  # 5mm from bottom

        can.rect(x, y, box_width, box_height)
        
        # Split text into multiple lines and draw each line
        line_height = 12
        y_position = y + box_height - line_height
        x_position = x + 5
        lines = '\n'.join([text, os.getenv('SIGN_TEXT'),sign_text]).split('\n')
        for line in lines:
            line = line.strip()  # Remove extra whitespace
            if line:  # Only draw non-empty lines
                can.drawString(x_position, y_position, line)
                y_position -= line_height
                
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)

        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

def process_pdf(input_file, input_path=None, output_path=None, vertical='bottom', horizontal='right', color='000080', text=''):
    if input_path is None:
        input_path = os.path.join('uploads', input_file.filename if hasattr(input_file, 'filename') else input_file)
    if output_path is None:
        output_path = os.path.join('processed', f'processed_{os.path.basename(input_path)}')
    
    if hasattr(input_file, 'save'):
        input_file.save(input_path)
    add_text_box_to_pdf(input_path, output_path, vertical, horizontal, color, text)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            vertical = request.form.get('vertical', 'bottom')
            horizontal = request.form.get('horizontal', 'right')
            color = request.form.get('color', '000080').lstrip('#')  # Default dark blue
            text = request.form.get('text', '')
            output_file = process_pdf(file, vertical=vertical, horizontal=horizontal, color=color, text=text)
            return send_file(output_file, mimetype='application/pdf', as_attachment=False)
    
    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    app.run(debug=True) 