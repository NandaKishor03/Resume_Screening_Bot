import React, { useState } from 'react';
import axios from 'axios';

function ResumeUpload() {
    const [JD, setJD] = useState("");
    const [resume, setResume] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        if (!JD || !resume) {
            setError("Please fill all fields");
            setLoading(false);
            return;
        }

        try {
            const formData = new FormData();
            formData.append("JD", JD);
            formData.append("resume", resume);

            const response = await axios.post("http://localhost:5000/upload", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            setResult(response.data.data);
        } catch (err) {
            setError(err.response?.data?.error || "Upload failed");
            console.error("Full error:", err.response?.data || err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h2>Resume Screening Bot</h2>
            
            {error && <div className="error">{error}</div>}
            
            <form onSubmit={handleSubmit}>
                <textarea
                    value={JD}
                    onChange={(e) => setJD(e.target.value)}
                    placeholder="Paste Job Description"
                    rows={6}
                    required
                />

                <input
                    type="file"
                    onChange={(e) => setResume(e.target.files[0])}
                    accept=".pdf,.doc,.docx"
                    required
                />

                <button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : 'Match Resume'}
                </button>
            </form>

            {result && (
                <div className="results">
                    <h3>Match Score: {result.match_score}%</h3>
                    {/* Render suggestions if available */}
                </div>
            )}
        </div>
    );
}

export default ResumeUpload;
