import streamlit as st
from pdf2image import convert_from_bytes, pdfinfo_from_bytes, exceptions
from PIL import Image
import io

# Title of the web app
st.title('PDF to JPG Converter')

# Step 1: File uploader to allow users to upload a PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    try:
        # Step 2: Convert PDF to images
        with st.spinner('Converting PDF to JPG...'):
            images = convert_from_bytes(uploaded_file.read())

        st.success('Conversion complete!')

        # Step 3: Display the images and allow downloading
        for i, image in enumerate(images):
            st.image(image, caption=f'Page {i + 1}', use_column_width=True)

            # Convert to bytes for downloading
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Step 4: Download button for each image
            st.download_button(
                label=f"Download Page {i + 1} as JPG",
                data=img_byte_arr,
                file_name=f"page_{i + 1}.jpg",
                mime="image/jpeg"
            )
    except exceptions.PDFInfoNotInstalledError as e:
        st.error("Poppler is not installed. Please install Poppler to use this feature.")
