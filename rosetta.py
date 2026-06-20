import streamlit as st
from PIL import Image
import io
import numpy as np

st.title("Rosetta Stone")
#UPLOAD THE IMAGE
upload_file = st.file_uploader("Upload File", type = ["png","jpeg","jpg","webp"])
#OPEN AND DISPLAY THE IMAGE
if upload_file is not None:
    img = Image.open(upload_file)
    st.image(img, caption = "Original Image")

    st.subheader("Conversion Subheader")

    #DROPDOWN DICTIONARY CHOICE MENU
    format_map = {#Choice on conversion type format [PIL format,file extension, MIME type]
        "PDF DOCUMENT": ["PDF", ".pdf", "application/pdf"],
        "PNG IMAGE": ["PNG", ".png", "image/png"],
        "JPEG IMAGE": ["JPEG",",jpg", "image/jpeg"],
        "WEBP": ["WEBP",".webp", "image/webp"]
    }
    
    #UI DROPDOWN
    user_choice = st.selectbox("Select output format", options=list(format_map.keys()))

    pil_format = format_map[user_choice][0]
    file_ext = format_map[user_choice][1]
    mime_type = format_map[user_choice][2]

    if pil_format in ["JPEG", "PDF"] and img.mode in ("RGBA"):
        img = img.convert("RGB")

    
    output_buffer = io.BytesIO()
    img.save(output_buffer, format = pil_format)

    st.download_button(
        label = f"Download {pil_format}",
        data = output_buffer.getvalue(),
        file_name= f"convertedfile.{file_ext}",
        mime = mime_type
    )