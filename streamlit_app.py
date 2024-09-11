import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

# Title of the web app
st.title('PDF to JPG Converter')

# Step 1: File uploader to allow users to upload a PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    # Step 2: Convert PDF to images using PyMuPDF
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    num_pages = pdf_document.page_count

    st.success(f'PDF loaded. Number of pages: {num_pages}')

    # Step 3: Display the images and allow downloading
    for page_num in range(num_pages):
        page = pdf_document.load_page(page_num)  # Get each page
        pix = page.get_pixmap()  # Convert page to image
        img = Image.open(io.BytesIO(pix.tobytes("png")))  # Convert image to Pillow Image format

        # Display image in the app
        st.image(img, caption=f'Page {page_num + 1}', use_column_width=True)

        # Convert image to bytes for download
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Step 4: Add a download button for each image
        st.download_button(
            label=f"Download Page {page_num + 1} as JPG",
            data=img_byte_arr,
            file_name=f"page_{page_num + 1}.jpg",
            mime="image/jpeg"
        )

    pdf_document.close()
