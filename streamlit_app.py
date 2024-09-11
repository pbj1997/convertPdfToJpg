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

    # Step 3: Collect images for individual downloads and add them to a ZIP file
    zip_buffer = io.BytesIO()  # In-memory buffer to store the ZIP file
    images = []  # To store each image for individual downloads

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)  # Get each page
            pix = page.get_pixmap()  # Convert page to image
            img = Image.open(io.BytesIO(pix.tobytes("png")))  # Convert image to Pillow Image format

            # Save image to byte array for both ZIP and individual download
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()

            # Add the image to the ZIP file
            zip_file.writestr(f"page_{page_num + 1}.jpg", img_bytes)

            # Store image byte array for individual download
            images.append((f"page_{page_num + 1}.jpg", img_bytes))

    pdf_document.close()

    # Step 4: Provide a download button for the ZIP file (at the top)
    zip_buffer.seek(0)  # Reset buffer position to the beginning
    st.download_button(
        label="Download All Pages as ZIP",
        data=zip_buffer,
        file_name="pdf_pages.zip",
        mime="application/zip"
    )

    # Step 5: Display images and provide individual download buttons
    for i, (file_name, img_bytes) in enumerate(images):
        # Display image in the app
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, caption=f'Page {i + 1}', use_column_width=True)

        # Add a download button for each individual image
        st.download_button(
            label=f"Download Page {i + 1} as JPG",
            data=img_bytes,
            file_name=file_name,
            mime="image/jpeg"
        )
