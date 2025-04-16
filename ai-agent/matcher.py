from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume(job_description, resume_text):
    """
    Match the job description with the resume using cosine similarity.
    Args:
    - job_description (str): The job description text.
    - resume_text (str): The resume text.

    Returns:
    - float: Cosine similarity score between the job description and the resume.
    """
    documents = [job_description, resume_text]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return round(similarity_matrix[0][0] * 100, 2)  # Return as percentage