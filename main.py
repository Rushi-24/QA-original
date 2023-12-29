from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import fitz  # PyMuPDF
import csv
from PIL import Image
import pytesseract
from transformers import pipeline
from transformers import AutoModelForQuestionAnswering
from transformers import AutoTokenizer


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

# Functions for reading PDF, CSV, and image
def read_pdf(file_path):
    pdf_text = ""
    pdf_document = fitz.open(file_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pdf_text += page.get_text()

    pdf_document.close()
    return pdf_text

def read_csv(file_path):
    csv_text = ""
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_text += ', '.join(row) + '\n'
    return csv_text

def read_image(file_path):
    image_text = pytesseract.image_to_string(Image.open(file_path))
    return image_text

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded file based on its type
        if filename.lower().endswith(".pdf"):
            text = read_pdf(file_path)
        elif filename.lower().endswith(".csv"):
            text = read_csv(file_path)
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            text = read_image(file_path)
        else:
            text = "Unsupported file format."

        return f"File '{filename}' has been uploaded and processed.\n\n{text}"
    
    model_name = "deepset/bert-large-uncased-whole-word-masking-squad2"

    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': "What is my name?",
        'context': text  }
    res = nlp(QA_input)

    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)


    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
