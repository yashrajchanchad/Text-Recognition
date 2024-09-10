from django.shortcuts import render

# Create your views here.
import easyocr
from PIL import Image
from django.shortcuts import render, redirect
from .forms import DocumentForm
import fitz  # PyMuPDF for PDF processing

# Function to extract text from an image using EasyOCR
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])  # Load English model
    results = reader.readtext(image_path)
    text = ' '.join([result[1] for result in results])
    return text

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = f"temp_page_{page_num}.png"
        pix.save(image_path)  # Save the page as an image
        text += extract_text_from_image(image_path)  # Extract text from the image
    return text

# Function to handle file uploads and text extraction
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file_type = document.file.url.split('.')[-1].lower()

            if file_type in ['png', 'jpg', 'jpeg']:
                extracted_text = extract_text_from_image(document.file.path)
            elif file_type == 'pdf':
                extracted_text = extract_text_from_pdf(document.file.path)
            else:
                extracted_text = "Unsupported file format."

            return render(request, 'result.html', {'text': extracted_text})
    else:
        form = DocumentForm()

    return render(request, 'upload.html', {'form': form})
