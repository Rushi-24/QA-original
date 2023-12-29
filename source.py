import os
import fitz  # PyMuPDF
import csv
from PIL import Image
import pytesseract
from transformers import pipeline

# Function to read PDF
def read_pdf(file_path):
    pdf_text = ""
    pdf_document = fitz.open(file_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pdf_text += page.get_text()

    pdf_document.close()
    return pdf_text

# Function to read CSV
def read_csv(file_path):
    csv_text = ""
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_text += ', '.join(row) + '\n'
    return csv_text

# Function to read image using OCR
def read_image(file_path):
    image_text = pytesseract.image_to_string(Image.open(file_path))
    return image_text

# Upload a file manually
uploaded_files_dir = 'static/files'  # Change this to your actual upload directory
files = os.listdir(uploaded_files_dir)

# Process the uploaded file
for file_name in files:
    file_path = os.path.join(uploaded_files_dir, file_name)

    if file_name.endswith(".pdf"):
        text = read_pdf(file_path)
    elif file_name.endswith(".csv"):
        text = read_csv(file_path)
    elif file_name.endswith((".png", ".jpg", ".jpeg")):
        text = read_image(file_path)
    else:
        text = "Unsupported file format."

    print(f"\nText from {file_name}:\n{text}")
    print("-" * 30)








