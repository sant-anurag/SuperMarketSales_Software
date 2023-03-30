import pytesseract
from PIL import Image
import PyPDF2

# Function to extract text from image using OCR
def ocr_extract(image_path):
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
    return text.strip()

# Function to extract text from normal PDF
def pdf_extract(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text.strip()

# Function to extract text from PDF with images
def pdf_with_images_extract(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        text = ''
        for page in reader.pages:
            for img in page.get_xobjects().values():
                if img['/Subtype'] == '/Image':
                    image = Image.frombytes(
                        mode='RGB',
                        size=(img['/Width'], img['/Height']),
                        data=img['/Filter'].decode('ascii')
                    )
                    text += ocr_extract(image)
            text += page.extract_text()
    return text.strip()

# Example usage
image_text = ocr_extract('image.png')
pdf_text = pdf_extract('document.pdf')
pdf_with_images_text = pdf_with_images_extract('document_with_images.pdf')
