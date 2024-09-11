import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import zipfile

# Title of the web app
st.title('PDF to JPG Converter')

# Step 1: File uploader to allow users to upload a PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    # Step 2: Convert PDF to images using PyMuPDF
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    num_pages = pdf_document.page_count

    st.success(f'PDF loaded. Number of pages: {num_pages}')

    # Step 3: Collect images and add them to a ZIP file
    zip_buffer = io.BytesIO()  # In-memory buffer to store the ZIP file
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)  # Get each page
            pix = page.get_pixmap()  # Convert page to image
            img = Image.open(io.BytesIO(pix.tobytes("png")))  # Convert image to Pillow Image format

            # Convert image to bytes for storing in ZIP
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Add the image to the ZIP file
            zip_file.writestr(f"page_{page_num + 1}.jpg", img_byte_arr)

    pdf_document.close()

    # Step 4: Provide a download button for the ZIP file
    zip_buffer.seek(0)  # Reset buffer position to the beginning
    st.download_button(
        label="Download All Pages as ZIP",
        data=zip_buffer,
        file_name="pdf_pages.zip",
        mime="application/zip"
    )
