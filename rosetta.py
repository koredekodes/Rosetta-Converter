import streamlit as st
from PIL import Image
import io
import fitz
import numpy as np

st.title("Rosetta")
#UPLOAD THE IMAGE
upload_file = st.file_uploader("Upload File", type = ["png","jpeg","jpg","webp", "pdf"])
#OPEN AND DISPLAY THE IMAGE
if upload_file is not None:
    if upload_file.type == "application/pdf":
        # Handle PDF file
        doc = fitz.open(stream=upload_file.read(), filetype="pdf")
        # Creates a slider if you want to convert multiple pages from the pdf
        if doc.page_count > 1:
            page_num = st.slider("Select Page to Convert", 1, doc.page_count,1)-1
        else:
            page_num = 0
        page = doc[page_num]
        
        img = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", (img.width, img.height), img.samples)
    else:
        img = Image.open(upload_file)
    st.image(img, caption = "Original Image")

    st.subheader("Conversion")

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
