import React, { useState } from 'react';
import axios from 'axios';
import './ResumeUpload.css'; // Import the CSS file

function ResumeUpload() {
  const [jobDescription, setJobDescription] = useState('');
  const [resume, setResume] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setResume(e.target.files[0].name); // Update the resume state with the file name
      const file = e.target.files[0]; // Get the selected file
      const formData = new FormData(); // Create a new FormData object
      formData.append('resume', file); // Append the file to the FormData object
      setResume(formData); // Update the resume state with the FormData object
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setResult(null);

    console.log('Submitting form...');
    console.log('Job Description:', jobDescription);
    console.log('Resume:', resume);

    if (!jobDescription ||!resume) {
      setError('Please provide both job description and resume');
      setLoading(false);
      return;
    }

    try {
      const formData = new FormData(); // Create a new FormData object
      formData.append('jd', jobDescription); // Append the job description
      if (resume instanceof FormData) { // Check if resume is a FormData object
        for (const pair of resume.entries()) { // Iterate over the resume FormData object
          formData.append(pair[0], pair[1]); // Append each pair to the new FormData object
        }
      } else {
        formData.append('resume', resume); // Append the resume file (if not a FormData object)
      }

      const response = await axios.post('http://localhost:5173/upload', formData, {
        headers: {...formData.getHeaders() },
        timeout: 30000, // 30 seconds timeout
      });

      if (response.status === 200) {
        setResult(response.data);
      } else {
        setError('Internal Server Error');
      }
    } catch (err) {
      setError('Internal Server Error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h2>Resume Screening System</h2>
      </div>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} className="form">
        <label>Job Description:</label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste job description here..."
          rows={10}
          cols={50}
          className="form-input"
        />
        <label>Resume:</label>
        <input
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx"
          className="form-input"
        />
        <button type="submit" disabled={loading} className="form-button">
          {loading? 'Processing...' : 'Upload and Match'}
        </button>
      </form>
      {result && (
        <div className="match-result">
          <h2>Match Result</h2>
          <p>Similarity Score: {result.similarity_score}</p>
          <ul>
            {result.entities.map((entity, index) => (
              <li key={index}>
                <span>{entity[0]} ({entity[1]})</span>
              </li>
            ))}
          </ul>
          <ul>
            {result.keywords.map((keyword, index) => (
              <li key={index}>
                <span>{keyword}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;