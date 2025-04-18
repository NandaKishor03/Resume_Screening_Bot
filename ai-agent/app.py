from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, CrossEncoder
from keybert import KeyBERT
import torch
import logging
import json
import spacy
from spacy import displacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import PyPDF2
import docx

app = Flask(__name__)
CORS(app)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load pre-trained models
sbert_model = SentenceTransformer('paraphrase-mpnet-base-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
keyword_model = KeyBERT(model=sbert_model)

# Load spaCy model for entity recognition
nlp = spacy.load('en_core_web_sm')

# /match endpoint
@app.route('/match', methods=['POST'])
def match_resume():
    try:
        print("Received request...")
        jd = request.form.get('jd')
        resume = request.files.get('resume')

        # Validate job description and resume
        if not jd or not resume:
            return jsonify({'error': 'Please provide both job description and resume'}), 400

        if not isinstance(jd, str) or not jd.strip():
            return jsonify({'error': 'Invalid job description'}), 400

        if not resume.filename or not resume.content_type:
            return jsonify({'error': 'Invalid resume file'}), 400

        # Extract entities from job description
        entities = extract_entities(jd)

        # Extract keywords from job description
        keywords = extract_keywords(jd)

        # Calculate similarity score
        similarity_score = calculate_similarity(resume, entities, keywords)

        return jsonify({
            'imilarity_score': similarity_score,
            'entities': entities,
            'keywords': keywords,
        })
    except Exception as e:
        logging.error(e)
        return jsonify({'error': str(e)}), 500

def extract_entities(jd):
    # Use spaCy for entity recognition
    doc = nlp(jd)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def extract_keywords(jd):
    # Use KeyBERT for keyword extraction
    keywords = keyword_model.extract_keywords(jd, top_n=10)
    return [keyword for keyword, _ in keywords]

def calculate_similarity(resume, entities, keywords):
    # Use Sentence Transformers for similarity calculation
    resume_text = extract_text_from_file(resume)
    similarity_score = 0
    for entity in entities:
        entity_text = entity[0]
        similarity = sbert_model.encode([entity_text, resume_text])
        similarity_score += similarity[0].dot(similarity[1])
    for keyword in keywords:
        keyword_text = keyword
        similarity = sbert_model.encode([keyword_text, resume_text])
        similarity_score += similarity[0].dot(similarity[1])
    return similarity_score / (len(entities) + len(keywords))

def extract_text_from_file(file):
    # Extract text from PDF, DOC, or DOCX file
    if file.content_type == 'application/pdf':
        # Use PyPDF2 for PDF files
        pdf_reader = PyPDF2.PdfReader(file.stream)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        # Use python-docx for DOC and DOCX files
        doc = docx.Document(file.stream)
        text = ''
        for para in doc.paragraphs:
            text += para.text
        return text
    else:
        return ''

if __name__ == '__main__':
    app.run(port=8000)