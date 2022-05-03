# %%
import streamlit as st
import streamlit.components as stc
# Utils
import fitz

st.title("Test signature addition")
st.header("Upload a pdf")
# upload a file to work with
uploaded_pdf = st.file_uploader("Choose a pdf file", type=['pdf'])
if uploaded_pdf is not None:
    doc = fitz.open(uploaded_pdf)
    try:
        areas = doc[-1].search_for("Customer")
        lastpage = doc[-1]
    except:
        try: 
            areas = doc[-2].search_for("Customer")
            lastpage = doc[-2]
        except:
            print("No signing field found")
try:
    st.write(areas)
except:
    st.write("no pdf selected")
st.header("Upload a png")
# %%
uploaded_png = st.file_uploader("Choose a png file", type=['png'])
if uploaded_png is not None:
    st.image(uploaded_png,width=250)
    x = 55
    y = 20
    rect = fitz.Rect(areas[0].x0, areas[0].y0-y, areas[0].x1+x, areas[0].y1+y)
    lastpage.insert_image(rect, filename = uploaded_png)
    document = doc.convert_to_pdf()
    filename = uploaded_pdf.name[:4] + "_signed" + ".pdf"
    st.download_button(label="Download PDF File", 
        data=document,
        file_name=filename,
        mime='application/octet-stream')