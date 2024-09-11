import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import os

# Set the title
st.title("PDF to JPG Converter")

# Upload the PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# If a file is uploaded
if uploaded_file is not None:
    # Display progress message
    with st.spinner("Converting PDF to images..."):
        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        
        # Convert PDF to images
        images = convert_from_path(temp_file_path)

        # Display images and give option to download them
        for i, image in enumerate(images):
            st.image(image, caption=f"Page {i+1}", use_column_width=True)

            # Convert to JPEG and provide download link
            img_path = os.path.join(tempfile.gettempdir(), f"page_{i+1}.jpg")
            image.save(img_path, "JPEG")

            with open(img_path, "rb") as img_file:
                btn = st.download_button(
                    label=f"Download Page {i+1} as JPG",
                    data=img_file,
                    file_name=f"page_{i+1}.jpg",
                    mime="image/jpeg"
                )

    # Remove temporary files
    os.remove(temp_file_path)
