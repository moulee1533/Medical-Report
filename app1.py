import os
import re
import pytesseract
from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Extract text from PDF or image
def extract_text(file_path, filename):
    if filename.lower().endswith('.pdf'):
        text = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ''
        return text
    else:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)

# Extract sugar values using regex
def find_sugar_values(text):
    results = {}

    fbs_match = re.search(r'(FBS|Fasting).*?(\d{2,3})', text, re.IGNORECASE)
    ppbs_match = re.search(r'(PPBS|Postprandial).*?(\d{2,3})', text, re.IGNORECASE)
    hba1c_match = re.search(r'(HbA1c).*?(\d\.\d)', text, re.IGNORECASE)

    if fbs_match:
        results['FBS'] = int(fbs_match.group(2))
    if ppbs_match:
        results['PPBS'] = int(ppbs_match.group(2))
    if hba1c_match:
        results['HbA1c'] = float(hba1c_match.group(2))

    return results

# Provide food and medical suggestions
def get_suggestions(data):
    suggestions = []

    fbs = data.get('FBS')
    ppbs = data.get('PPBS')
    hba1c = data.get('HbA1c')

    if fbs and fbs >= 126:
        suggestions.append(("High FBS", "Avoid refined carbs, walk daily, drink fenugreek water."))
    elif fbs and 100 <= fbs < 126:
        suggestions.append(("Prediabetic FBS", "Eat oats, avoid sugary snacks, check again in 1 month."))

    if ppbs and ppbs >= 200:
        suggestions.append(("High PPBS", "Avoid fruit juice, prefer green salads before meals."))
    elif ppbs and 140 <= ppbs < 200:
        suggestions.append(("Prediabetic PPBS", "Control portions, walk after meals, cut sweets."))

    if hba1c and hba1c >= 6.5:
        suggestions.append(("Diabetic HbA1c", "Low-GI diet, split meals, consult doctor."))
    elif hba1c and 5.7 <= hba1c < 6.5:
        suggestions.append(("Prediabetic HbA1c", "Limit sugar intake, test every 3 months."))

    return suggestions

# Determine risk level
def get_risk_level(data):
    level = "Normal"
    if data.get("HbA1c", 0) >= 6.5 or data.get("FBS", 0) >= 126 or data.get("PPBS", 0) >= 200:
        level = "High Risk"
    elif data.get("HbA1c", 0) >= 5.7 or data.get("FBS", 0) >= 100 or data.get("PPBS", 0) >= 140:
        level = "Moderate Risk"
    return level

# Create PDF report
def generate_pdf(file_path, data, tips, risk_level):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Medical Report Summary")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Extracted Values:")
    y -= 20
    c.setFont("Helvetica", 12)
    for k, v in data.items():
        c.drawString(70, y, f"{k}: {v}")
        y -= 20

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Risk Level: {risk_level}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Suggestions:")
    y -= 20
    c.setFont("Helvetica", 12)
    for tip in tips:
        c.drawString(70, y, f"• {tip[0]}: {tip[1]}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

# Route: main page
@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_data = {}
    tips = []
    risk = ""
    pdf_filename = ""

    if request.method == 'POST':
        file = request.files['report']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            text = extract_text(filepath, filename)
            extracted_data = find_sugar_values(text)
            tips = get_suggestions(extracted_data)
            risk = get_risk_level(extracted_data)

            pdf_filename = "report_summary.pdf"
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            generate_pdf(pdf_path, extracted_data, tips, risk)

    return render_template('index.html', results=extracted_data, tips=tips, risk=risk, pdf_url=pdf_filename)

# Route: serve the PDF file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
