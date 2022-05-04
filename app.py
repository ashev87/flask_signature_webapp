# %%
import streamlit as st
import fitz
from PIL import Image
import numpy as np

st.title("Adding signature to pdf document")
st.header("Upload a pdf")
# upload a file to work with
uploaded_pdf = st.file_uploader("Choose a pdf file", type='pdf', accept_multiple_files = False)
# for debug show filedata to screen
# st.json(dict(uploaded_object = uploaded_pdf))
if uploaded_pdf is not None:
    # use this for local use
    #doc = fitz.open(uploaded_pdf)
    # use this to stream ioBytes data to fitz
    doc = fitz.open("pdf", uploaded_pdf.getvalue())
    # find Customer field in the document
    try:
        areas = doc[-1].search_for("Customer")
        lastpage = doc[-1]
    except:
        try: 
            areas = doc[-2].search_for("Customer")
            lastpage = doc[-2]
        except:
            print("No signing field found")
# try:
#     st.write(areas)
# except:
#     st.write("no pdf selected")
# %%
st.header("Upload a png")
uploaded_png = st.file_uploader("Choose a png file", type=['png'])
if uploaded_png is not None:
    st.image(uploaded_png,width=250)
    # adjust signing place
    x = 55
    y = 20
    rect = fitz.Rect(areas[0].x0, areas[0].y0-y, areas[0].x1+x, areas[0].y1+y)
    # insert image as stream ioBytes to the pdf document
    lastpage.insert_image(rect, stream = uploaded_png.getvalue())
    # save document locally
    document = doc.convert_to_pdf()
    filename = uploaded_pdf.name[:4] + "_signed" + ".pdf"
    st.download_button(label="Download PDF File", 
        data=document,
        file_name=filename,
        mime='application/octet-stream')