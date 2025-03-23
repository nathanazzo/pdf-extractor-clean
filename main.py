from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['file']
    filename = secure_filename(pdf_file.filename)

    try:
        pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        full_text = ""

        for page in pdf_doc:
            full_text += page.get_text()

        return jsonify({'text': full_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500