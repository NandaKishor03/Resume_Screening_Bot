# The Flask app that will receive file uploads, process them using parser.py and matcher.py, and return the parsed and matched data.

from flask import Flask, request, jsonify
import os
from parser import parse_file
from matcher import match_resume

app = Flask(__name__)

UPLOADED_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOADED_FOLDER

@app.route('/upload', method=["POST"])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No File part of the request'}), 400
    
    file = request.files['files']

    if file.filename == "":
        return jsonify({'error': 'No File Selected'}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
    file.save(file.path)

    # Parse the uploaded file (PDF or DOCX)
    extracted_text = parse_file(file_path)

    # Dummy job description (can be replaced with actual job description)
    # job_description = """
    # Looking for a skilled data scientist with experience in Python, machine learning, and data analysis.
    # Must have knowledge of data visualization and statistical analysis.
    # """

    # Match the parsed resume text with the given job description
    match_score = match_resume(JD , extracted_text)

    os.remove(file_path)  # Clean up the uploaded file after processing

    return jsonify({
        'Extracted Text' : extracted_text,
        'Match Score' : match_score
    }), 200

if __name__ == (__main__):
    if not os.path.exists(UPLOADED_FOLDER):
        os.makedirs(UPLOADED_FOLDER)
    app.run(debug=True, port=5000)

    





#  How It Works Now:

# Job Description is sent by the user (from frontend) as part of the form-data along with the resume file.

# The server then parses the resume, and matches it against the user-provided JD using the logic in matcher.py.

# Returns:

# The extracted text from the resume.

# The match score (how well the resume matches the JD).
