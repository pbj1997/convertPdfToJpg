import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io

# Title
st.title('PDF to JPG Converter')

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    # Convert PDF to images
    images = convert_from_bytes(uploaded_file.read())

    # Display and download converted images
    for i, image in enumerate(images):
        st.image(image, caption=f'Page {i + 1}', use_column_width=True)

        # Download button
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        st.download_button(
            label=f"Download Page {i + 1} as JPG",
            data=img_byte_arr,
            file_name=f"page_{i + 1}.jpg",
            mime="image/jpeg"
        )
