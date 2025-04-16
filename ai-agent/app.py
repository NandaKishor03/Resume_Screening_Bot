# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import PyPDF2
# import docx
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'flask_uploads'
# ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

# def extract_text_from_docx(docx_path):
#     doc = docx.Document(docx_path)
#     return "\n".join([para.text for para in doc.paragraphs])

# @app.route('/match', methods=["POST"])
# def upload_file():
#     print("Request content type:", request.content_type)
#     print("Request headers:", request.headers)
    
#     if 'resume' not in request.files:
#         print("No resume in request.files")
#         return jsonify({'error': 'No resume file uploaded'}), 400
    
#     file = request.files['resume']
#     jd_text = request.form.get('JD', "")

#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if not allowed_file(file.filename):
#         return jsonify({'error': 'Invalid file type'}), 400

#     try:
#         if not os.path.exists(UPLOAD_FOLDER):
#             os.makedirs(UPLOAD_FOLDER)
            
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)

#         if file.filename.endswith('.pdf'):
#             extracted_text = extract_text_from_pdf(file_path)
#         elif file.filename.endswith('.docx'):
#             extracted_text = extract_text_from_docx(file_path)

#         if not jd_text.strip():
#             os.remove(file_path)
#             return jsonify({'error': 'Job description required'}), 400

#         vectorizer = TfidfVectorizer(stop_words='english')
#         tfidf_matrix = vectorizer.fit_transform([jd_text, extracted_text])
#         cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
#         match_score = round(cosine_sim[0][0] * 100, 2)

#         os.remove(file_path)

#         return jsonify({
#             'match_score': match_score,
#             'suggestions': [],
#             'missing_keywords': []
#         })

#     except Exception as e:
#         if 'file_path' in locals() and os.path.exists(file_path):
#             os.remove(file_path)
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(host='0.0.0.0', port=5001, debug=True)













# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import os
# # import PyPDF2
# # import docx
# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity
# # import re

# # app = Flask(__name__)
# # CORS(app)

# # UPLOAD_FOLDER = 'flask_uploads'
# # ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # def extract_text_from_pdf(pdf_path):
# #     text = ""
# #     with open(pdf_path, 'rb') as file:
# #         reader = PyPDF2.PdfReader(file)
# #         for page in reader.pages:
# #             text += page.extract_text()
# #     return text

# # def extract_text_from_docx(docx_path):
# #     doc = docx.Document(docx_path)
# #     return "\n".join([para.text for para in doc.paragraphs])

# # def calculate_match(jd_text, resume_text):
# #     vectorizer = TfidfVectorizer(stop_words='english')
# #     tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
# #     cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
# #     return round(cosine_sim[0][0] * 100, 2)

# # @app.route('/match', methods=["POST"])
# # def upload_file():
# #     print("Received request with files:", request.files)
# #     print("Received form data:", request.form)
    
# #     if 'resume' not in request.files:
# #         return jsonify({'error': 'No resume file uploaded'}), 400
    
# #     file = request.files['resume']
# #     jd_text = request.form.get('JD', "")

# #     if file.filename == '':
# #         return jsonify({'error': 'No selected file'}), 400

# #     if not allowed_file(file.filename):
# #         return jsonify({'error': 'Invalid file type'}), 400

# #     try:
# #         if not os.path.exists(UPLOAD_FOLDER):
# #             os.makedirs(UPLOAD_FOLDER)
            
# #         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
# #         file.save(file_path)

# #         if file.filename.endswith('.pdf'):
# #             extracted_text = extract_text_from_pdf(file_path)
# #         elif file.filename.endswith('.docx'):
# #             extracted_text = extract_text_from_docx(file_path)

# #         if not jd_text.strip():
# #             os.remove(file_path)
# #             return jsonify({'error': 'Job description required'}), 400

# #         match_score = calculate_match(jd_text, extracted_text)
# #         os.remove(file_path)

# #         return jsonify({
# #             'match_score': match_score,
# #             'suggestions': [],
# #             'missing_keywords': []
# #         }), 200

# #     except Exception as e:
# #         if os.path.exists(file_path):
# #             os.remove(file_path)
# #         return jsonify({'error': str(e)}), 500

# # if __name__ == '__main__':
# #     if not os.path.exists(UPLOAD_FOLDER):
# #         os.makedirs(UPLOAD_FOLDER)
# #     app.run(host='0.0.0.0', port=5001, debug=True)


















from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parser import parse_file
from matcher import match_resume

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'flask_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/match', methods=["POST"])
def upload_file():
    print("\n==== New Request ====")
    print("Headers:", request.headers)
    print("Form data:", request.form)
    print("Files:", request.files)
    
    if 'resume' not in request.files:
        print("ERROR: No resume in request.files")
        return jsonify({'error': 'No resume file in request'}), 400
    
    file = request.files['resume']
    jd_text = request.form.get('JD', "")

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        print(f"File saved to: {file_path}")

        extracted_text = parse_file(file_path)
        match_score = match_resume(jd_text, extracted_text)
        
        os.remove(file_path)
        
        return jsonify({
            'match_score': match_score,
            'suggestions': [],
            'missing_keywords': []
        })

    except Exception as e:
        print(f"ERROR: {str(e)}")
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5001, debug=True)