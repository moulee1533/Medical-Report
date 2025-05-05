# Medical Report Analyzer 🩺📑💊

An AI-powered web application designed to scan and analyze medical reports to provide personalized health suggestions. It uses NLP to extract key information and recommends suitable food and medicine based on the data extracted from the reports.

## 🚀 Features

- 📄 Upload and scan medical reports (PDF/Image)
- 🧠 Extracts key health data using OCR + NLP
- 🥗 Provides food and diet suggestions
- 💊 Suggests possible medicines (non-prescriptive)
- 🌐 User-friendly web interface

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Libraries & Tools:** EasyOCR, pytesseract, spaCy, OpenCV, Pandas, Flask

## 📁 Project Structure

medical-report-analyzer/

├── app.py # Flask backend

├── analyzer.py # Report analysis and suggestion logic

├── templates/

│ └── index.html # Web interface

├── static/

│ └── style.css # Styling for frontend

├── utils/

│ └── food_medicine_suggester.py # Suggestion engine

├── uploads/ # Uploaded reports

├── requirements.txt # Python dependencies




## ⚙️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/medical-report-analyzer.git
   cd medical-report-analyzer
    Install Required Libraries


    pip install -r requirements.txt
    Install OCR Tools
    
    EasyOCR


    pip install easyocr
    Tesseract
    
    Install Tesseract OCR and ensure it's added to system PATH.
    
    Run the Flask App




    python app.py
    Access the App
    
    Open your browser and go to http://localhost:5000

📷 Supported Input Formats
    PDF Reports
    
    Scanned Image Reports (JPG, PNG)

🧪 Example Use Cases
    Patient health recommendation system
    
    Clinics or hospitals for report preprocessing
    
    Telemedicine support tools

🙌 Acknowledgements
    EasyOCR
    
    Tesseract OCR
    
    Flask
    
    spaCy
