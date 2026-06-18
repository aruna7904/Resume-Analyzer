from pypdf import PdfReader
import io

def extract_text_from_pdf(file_storage_object):
    """
    Extracts raw text data dynamically from stream binaries without writing to disk buffers.
    """
    try:
        pdf_file = io.BytesIO(file_storage_object.read())
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error parsing PDF structural data: {str(e)}")