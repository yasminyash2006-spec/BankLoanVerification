from flask import Flask, render_template, request

import pytesseract 
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd=r"c:\program files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

verification_result = "original"
application_no = "LN2026001"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['document']
        filename = file.filename
        file.save('uploads/' + file.filename)
        return "Uploaded File Name : " + filename

    return render_template('upload.html')


@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/ocr_test')
def ocr_test():

    global verification_result
    global application_no

    image = Image.open("uploads/test_fake.png")

    text = pytesseract.image_to_string(image)

    print("OCR TEXT:", text)

    if "LN2026001" in text:
        verification_result = "Original"
        application_no = "LN2026001"
        result = "Original Document"
    else:
        verification_result = "Fake"
        application_no = "Fake"
        result = "Fake Document"

    return f"""
    <h2>OCR Verification Result</h2>
    <h3>{result}</h3>
    <p>Application No: {application_no}</p>
    <p>Verification: {verification_result}</p>
    <a href="/status">View Status</a>
    """
    
@app.route('/result', methods=['POST'])
def result():
    return "<h2>Verification Result</h2><h3>Demo Result: Document Verified Successfully ✅</h3>"

@app.route('/status')
def status():
   
    if verification_result =="Original":
        status_text = "Verified"
        loan_status = "Approved"
    else:
        status_text = "Not Verified"
        loan_status = "Unapproved"

    return f"""
    <h1>Loan Verification Status</h1>
    <hr>
    <h3>Application No: {application_no}</h3>
    <p>Document Verification: Completed</p>
    <p>OCR Verification: Completed</p>
    <p>Status: <b>{status_text}</b></p>
    <p>Loan Status: <b>{loan_status}</b></p>
    """

if __name__ == '__main__':
    app.run(debug=True)
