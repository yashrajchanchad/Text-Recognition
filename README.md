# Django OCR Project - Text Extraction from PDFs and Images Using EasyOCR

This project is a web-based application that extracts text from PDF files and images using **EasyOCR**. It allows users to upload an image or PDF file and returns the extracted text.

## Features
- Extract text from **PDF** files and **images** (PNG, JPEG, etc.).
- Supports English OCR with **EasyOCR**.
- Uses **Bootstrap** for a clean and responsive UI.
- Supports multiple file types (PDF, JPG, PNG).
- Converts PDF pages into images before extracting text.

---

## Prerequisites

Ensure you have the following installed:
- **Python 3.6+**
- **Django 4.x**
- **Pip** for installing dependencies

## Required Libraries

Install the following libraries before running the project:

1. **Django** (for the web framework)
2. **EasyOCR** (for the text extraction)
3. **Pillow** (for image handling in Django)
4. **PyMuPDF** (for converting PDF pages to images)

You can install all required libraries by running the following command:

```bash
pip install django easyocr Pillow pymupdf
```

---

## Project Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/ocr-project.git
cd ocr-project
```

### 2. **Set Up a Virtual Environment (Optional but Recommended)**

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
```

### 3. **Install Dependencies**
Run the following command to install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. **Set Up the Django Project**

Create the required migrations and migrate the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. **Run the Development Server**

Start the Django development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/ocr/` to access the application.

---

## How the Project Works

### 1. **File Upload Form (Upload a File)**

The file upload form allows users to upload a PDF or image file. Once uploaded, the file is processed based on its type:
- **Image files**: Directly processed by **EasyOCR** to extract text.
- **PDF files**: Each page of the PDF is converted into an image using **PyMuPDF**, and the text is extracted from these images using **EasyOCR**.

#### Views in `views.py`:
- **upload_file**: This view handles file uploads and extracts the text from the uploaded document.

```python
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
```

### 2. **Text Extraction Functions**

- **extract_text_from_image**: This function takes an image file path, uses **EasyOCR** to detect and extract text from the image, and returns the result.

```python
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])  # Load English model
    results = reader.readtext(image_path)
    text = ' '.join([result[1] for result in results])
    return text
```

- **extract_text_from_pdf**: This function takes a PDF file path, converts each page into an image using **PyMuPDF**, and extracts text from each image.

```python
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
```

### 3. **Templates (Frontend)**

The project uses **Bootstrap** for styling and responsiveness.

- **Upload Form** (`upload.html`): This page provides a simple form for users to upload a file.
- **Result Page** (`result.html`): This page displays the extracted text from the uploaded document.

---

## Running the Project

1. Run the following command to start the development server:
```bash
python manage.py runserver
```

2. Navigate to `http://127.0.0.1:8000` to upload an image or PDF file.
3. The system will display the extracted text after processing.

---

## Notes

- **EasyOCR** supports multiple languages. To add more languages, modify the `Reader` initialization in the `extract_text_from_image` function.
- PDF processing is done by converting each page to an image before text extraction.

Feel free to contribute or report issues!