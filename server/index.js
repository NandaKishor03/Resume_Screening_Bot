// const express = require('express');
// const cors = require('cors');
// const axios = require('axios');
// const multer = require('multer');
// const fs = require('fs');
// const path = require('path');
// const FormData = require('form-data');
// const PORT = 5000;

// const app = express();
// app.use(cors());

// // File upload settings
// const storage = multer.diskStorage({
//     destination: (req, file, callback) => {
//         callback(null, 'uploads/');
//     },
//     filename: (req, file, callback) => {
//         callback(null, Date.now() + '-' + file.originalname);
//     }
// });

// // File size limit (10MB as an example)
// const upload = multer({ 
//     storage,
//     limits: { fileSize: 10 * 1024 * 1024 }, // Max file size 10MB
//     fileFilter: (req, file, callback) => {
//         const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
//         if (!allowedTypes.includes(file.mimetype)) {
//             return callback(new Error('Only PDF or Word files are allowed'), false);
//         }
//         callback(null, true);
//     }
// });

// if (!fs.existsSync('uploads')) {
//     fs.mkdirSync('uploads');
// }

// app.post('/upload', upload.single('resume'), (req, res) => {
//     try {
//         const resumepath = req.file?.path;  // The uploaded file path
//         const jd = req.body.JD;  // The job description

//         // Error handling for missing resume or JD
//         if (!resumepath || !jd) {
//             return res.status(400).send("Missing file or job description");
//         }

//         const formData = new FormData();
//         formData.append('JD', jd);
//         formData.append('resume', fs.createReadStream(resumepath));

//         // Send formData to another API
//         axios.post("http://localhost:5001/match", formData, {
//             headers: {
//                 ...formData.getHeaders(),
//                 'Content-Length': req.file.size
//             },
//             timeout:30000
//         })
//         .then(response => {

//             if (response.data_.match_score){
//                 throw new Error("Invalid Response from API Service");
//             }

//             fs.unlink(resumepath , (err) => {
//                 if (err) console.error('Error deleting file:', err);
//             });

//             res.json({
//                 success: true,
//                 data: {
//                     score: response.data.match_score,
//                     // suggestions: response.data.suggestions || [],
//                     missing: response.data.missing_keywords || []
//                 }
//             });
//         })
//         .catch(err => {
//             console.error('API Error:', err.response?.data || err.message);
//             // Change 6: More detailed error response
//             res.status(500).json({ 
//                 error: "Processing failed",
//                 details: err.response?.data?.error || err.message
//             });
//         });

//     } catch (err) {
//         console.error('Upload Error:', err);
//         res.status(500).json({ 
//             error: "Upload failed",
//             details: err.message 
//         });
//     }
// });
// app.listen(PORT, () => {
//     console.log(`Server is running on http://localhost:${PORT}`);
// });













const express = require('express');
const cors = require('cors');
const axios = require('axios');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');
const PORT = 5000;

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        if (!fs.existsSync('uploads')) {
            fs.mkdirSync('uploads');
        }
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({
    storage,
    limits: { fileSize: 10 * 1024 * 1024 },
    fileFilter: (req, file, cb) => {
        const allowedTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ];
        if (!allowedTypes.includes(file.mimetype)) {
            return cb(new Error('Only PDF/DOCX files allowed'), false);
        }
        cb(null, true);
    }
});

app.post('/upload', upload.single('resume'), async (req, res) => {
    try {
        console.log('Received file:', req.file);
        console.log('Received JD:', req.body.JD);

        if (!req.file || !req.body.JD) {
            return res.status(400).json({ error: "Missing file or JD" });
        }

        const formData = new FormData();
        // Add JD as a field
        formData.append('JD', req.body.JD);
        // Add file with proper options
        formData.append('resume', fs.createReadStream(req.file.path), {
            filename: req.file.originalname,
            contentType: req.file.mimetype,
            knownLength: req.file.size
        });

        const headers = {
            ...formData.getHeaders(),
            'Content-Length': await new Promise((resolve) => {
                formData.getLength((err, length) => {
                    if (err) resolve(undefined);
                    else resolve(length);
                });
            })
        };

        const response = await axios.post("http://localhost:5001/match", formData, { 
            headers,
            maxContentLength: Infinity,
            maxBodyLength: Infinity,
            timeout: 30000
        });

        fs.unlink(req.file.path, () => {});

        res.json(response.data);

    } catch (err) {
        console.error('Full error:', err.stack);
        if (req.file?.path) fs.unlink(req.file.path, () => {});
        res.status(500).json({ 
            error: "Processing failed",
            details: err.response?.data || err.message
        });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});