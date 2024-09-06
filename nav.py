import streamlit as st

def Navbar():
    with st.sidebar:
        st.page_link('main.py', label="Home Page")
        st.page_link('pages/ppt_extract.py', label="Powerpoint Image Extracter")
        st.page_link('pages/video_tool.py', label="Video Download Tool")