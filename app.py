import fitz  # PyMuPDF
import json
from flask import Flask, request, jsonify, send_from_directory
import os
from transformers import pipeline

app = Flask(__name__)

# Directory containing the PDFs and static files
pdf_dir = 'C:/Users/UTENTE/LineeGUIDATIp/pdf'
static_dir = 'C:/Users/UTENTE/LineeGUIDATIp'

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract and save text to JSON
def save_text_to_json(pdf_path, json_path):
    text = extract_text_from_pdf(pdf_path)
    data = {"content": text}
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# PDF and JSON file paths
pdf_files = [
    ("REV.2024.01.02 Linee guida.pdf", "linee_guida.json"),
    ("2024.01.02 PROCEDURE ATIPROJECT.pdf", "procedure.json"),
    ("2024.01.02 VALIDAZIONE ZUCCHETTI E CALENDARIO ASSENZE.pdf", "validazione.json")
]

# Extract texts from PDFs
for pdf, json_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf)
    save_text_to_json(pdf_path, json_file)

# Load extracted data from JSON files
def load_data():
    with open('linee_guida.json', 'r', encoding='utf-8') as f:
        linee_guida_data = json.load(f)['content']
    with open('procedure.json', 'r', encoding='utf-8') as f:
        procedure_data = json.load(f)['content']
    with open('validazione.json', 'r', encoding='utf-8') as f:
        validazione_data = json.load(f)['content']
    return linee_guida_data, procedure_data, validazione_data

linee_guida_data, procedure_data, validazione_data = load_data()

# Configure Hugging Face model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Function to find the answer
def find_answer(data, question):
    result = qa_pipeline(question=question, context=data)
    return result['answer']

@app.route('/chatbot', methods=['POST'])
def chatbot():
    question = request.json.get('question')
    response = find_answer(linee_guida_data, question)
    if not response:
        response = find_answer(procedure_data, question)
    if not response:
        response = find_answer(validazione_data, question)
    return jsonify({'response': response})

@app.route('/')
def serve_index():
    return send_from_directory(static_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(static_dir, path)

if __name__ == '__main__':
    app.run(debug=True)
