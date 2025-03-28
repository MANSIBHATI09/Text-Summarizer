from flask import Flask, render_template, request
from textSummary import summarizer
import PyPDF2  # or `import fitz` for PyMuPDF

app = Flask(__name__)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extractText()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        pdf_file = request.files.get('pdf_file')
        
        if pdf_file:
            rawtext = extract_text_from_pdf(pdf_file)
        
        summary, original_txt, len_orig_txt, len_summary = summarizer(rawtext)
        
    return render_template('summary.html', summary=summary, original_txt=original_txt, len_orig_txt=len_orig_txt, len_summary=len_summary)

if __name__ == "__main__":
    app.run(debug=True)
