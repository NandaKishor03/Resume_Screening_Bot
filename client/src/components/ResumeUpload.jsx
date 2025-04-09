import React, { useState } from 'react';
import axios from 'axios';


function ResumeUpload() {
    const [JD, setJD] = useState("");
    const [resume, setResume] = useState("");
    const [result, setResult] = useState("");

    const handleSubmit=  (e) => {
        e.preventDefault();

        if (!JD || !resume){
            alert("Please fill in all fields");
            return;
        }

        const formData = new FormData();
        formData.append("JD",JD);
        formData.append("resume",resume);

        axios.post("https://localhost:6666/upload",formData)
        .then((result)=>{
            console.log(result.data)
            setResult(result.data);
        })
        .catch((err) => {
            console.error(err);
        })
    }

    return (    

        <div>
            <h2>Resume Screening Bot</h2>
            <form action="POST" onSubmit={handleSubmit} ></form>

            <textarea name="JD_info" id="jd" rows={6} value={JD} onChange={(e) => setJD(e.target.value)} placeholder="Paste the Job Description here" required/>

            <input type="file" onChange={(e) => setResume(e.target.files[0])} accept='.pdf,.doc,.docx' required/>

            <button type='submit'>Match Resume</button>

            {result && (
                <div style={{
                    marginTop: '20px',
                    padding: '16px',
                    border: '2px solid #4caf50',
                    borderRadius: '8px',
                    backgroundColor: '#e8f5e9',
                    width: '80%',
                    marginLeft: 'auto',
                    marginRight: 'auto',
                    textAlign: 'left'
                }}>
                    <h3>Match Score: <span style={{ color: '#2e7d32' }}>{result.match_score}</span></h3>
                    <h4>Suggestions:</h4>
                    <ul>
                    {result.suggestions.split('\n').map((s, index) => (
                        <li key={index}>{s}</li>
                    ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default ResumeUpload;