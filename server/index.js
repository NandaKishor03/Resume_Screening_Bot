const express = require('express');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 5173;

// Middleware
app.use(cors());
app.use(express.json());

// Multer for file uploads
const upload = multer({
  dest: './uploads/',
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter(req, file, cb) {
    if (!file.originalname.match(/\.(pdf|doc|docx)$/)) {
      return cb(new Error('Only PDF, DOC, and DOCX files are allowed'));
    }
    cb(null, true);
  },
});

// /upload endpoint
app.post('/upload', upload.single('resume'), async (req, res) => {
  try {
    console.log("Data Received:");
    console.log(req.body); // Should now contain the job description
    console.log(req.file); // Should now contain the uploaded file

    const { jd } = req.body;
    const resume = req.file;

    if (!jd ||!resume) {
      return res.status(400).json({ error: 'Please provide both job description and resume' });
    }

    // Validate job description and resume
    if (typeof jd!== 'tring' ||!jd.trim()) {
      return res.status(400).json({ error: 'Invalid job description' });
    }

    if (!resume.originalname ||!resume.path) {
      return res.status(400).json({ error: 'Invalid resume file' });
    }

    // Call Python API for matching
    const pythonApiUrl = 'http://localhost:8000/match';

    const formData = new FormData();
    formData.append('jd', jd);
    formData.append('resume', resume.buffer);

    const response = await axios.post(pythonApiUrl, formData, {
      headers: {...formData.getHeaders() },
      timeout: 30000, // 30 seconds timeout
    });

    if (response.status === 200) {
      console.log('Python API response Successfull:', response.data);
      return res.json(response.data);
    } else {
      return res.status(500).json({ error: 'Internal Server Error' });
    }
  } catch (err) {
    console.error('Error:', err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});