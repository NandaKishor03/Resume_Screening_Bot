const express = require('express');
const cors = require('cors');
const axios = require('axios');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const PORT = 6666;

const app = express();
app.use(cors());

const storage = multer.diskStorage({
    destination: (req,file,cd) => {
        cd(null,'uploads/');
    },
    filename:(req,file,cd) => {
        cb(null,Date.now()+'-'+
        file.originalname);
    }
});

const upload = multer({storage});

if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}

app.post('/upload',upload.single('resume'),(req,res) =>{
    const resumepath = req.file.path;
    const jd = req.body.JD;

    const formData = new FormData();
    formData.append("JD",jd);
    formData.append("resume",fs.createReadStream(resumepath));
})

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});