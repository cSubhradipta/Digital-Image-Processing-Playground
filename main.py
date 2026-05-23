import streamlit as st #type: ignore
import numpy as np
from PIL import Image
import streamlit.components.v1 as components #type:ignore

from config import *
from utils import * # Updated to match your new naming convention

st.set_page_config(
    layout="wide",
    page_title="Digital Image Processing Playground"
)

st.markdown("""
    <style>
        .topbar {
            position: fixed; 
            top: 15px;
            left: 0;
            width: 100vw; 
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 999999;
            pointer-events: none; 
            transition: opacity 0.3s ease-in-out; 
            opacity: 1; 
        }
        
        .topbar-title {
            font-size: 24px;
            font-weight: 600; 
            letter-spacing: 0.5px; 
            color: #f3f4f6;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.3); 
            transform: translateX(160px); 
        }

        .block-container {
            padding-top: 5.5rem !important; 
            padding-bottom: 3rem !important;
            min-height: 100vh; 
            display: flex;
            flex-direction: column;
            justify-content: flex-start; 
        }

        [data-testid="stMain"] .block-container > div {
            display: flex;
            flex-direction: column;
            justify-content: flex-start; 
            flex-grow: 1;
        }

        [data-testid="stMain"] [data-testid="stVerticalBlock"] {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            margin-top: auto !important;
            margin-bottom: auto !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stImage"] {
            display: flex;
            justify-content: center; 
            width: auto !important; 
            max-width: 90% !important;
        }
        
        [data-testid="stImage"] img {
            max-height: 70vh !important; 
            border-radius: 8px !important;
        }

        div[data-testid="stDialog"] [data-testid="stImage"] img {
            max-height: 60vh !important; 
            max-width: 100vh !important;
        }

        [data-testid="stSidebar"] {
            min-width: 320px !important;
            max-width: 320px !important;
            overflow: hidden !important;
        }
        
        [data-testid="stSidebarHeader"] {
            padding: 0px !important;
            height: 0px !important;
            display: none !important;
        }
        
        [data-testid="stSidebarUserContent"] {
            padding-top: 1.5rem !important;
            padding-bottom: 0 !important;
            padding-left: 1.2rem !important; 
            padding-right: 1.2rem !important;
            gap: 0.2rem !important; 
        }

        [data-testid="stFileUploader"] {
            min-height: 0px !important;
            margin-bottom: 0px !important;
        }
        
        [data-testid="stFileUploader"] section {
            padding: 0px !important;
            height: 38px !important;
            min-height: 38px !important;
            background-color: transparent !important;
            border: 1px solid rgba(250, 250, 250, 0.2) !important;
            border-radius: 8px !important;
            position: relative !important;
            cursor: pointer !important;
            overflow: hidden !important;
        }
        
        [data-testid="stFileUploader"] section > * {
            opacity: 0 !important;
            position: absolute !important;
            top: 0; left: 0;
            width: 100% !important;
            height: 100% !important;
            z-index: 99 !important;
            cursor: pointer !important;
        }
        
        [data-testid="stFileUploader"] section::after {
            content: "Upload";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 14px;
            font-weight: 400;
            color: #fafafa;
            z-index: 1;
            pointer-events: none; 
        }

        [data-testid="stUploadedFileList"],
        [data-testid="stFileUploader"] > div:last-child {
            display: none !important;
        }
        
        .stButton button {
            height: 38px !important;
            min-height: 38px !important;
            padding: 0px 10px !important;
            font-size: 14px !important;
            border-radius: 8px !important;
        }

        .stSelectbox label, .stSlider label {
            font-size: 13px !important;
            margin-bottom: 2px !important; 
            color: #d1d5db; 
        }
        div[data-baseweb="select"] > div {
            padding: 0px 8px !important;
            min-height: 34px !important;
            font-size: 13px !important;
            border-radius: 6px !important;
        }
        .stSlider {
            margin-bottom: -10px !important; 
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
        
        [data-testid="stSelectbox"] {
            margin-top: -20px;
            margin-bottom: 8px;
        }
 
        [data-testid="stSlider"] {
            margin-top: -16px;
        }

        [data-testid="stSidebar"] [data-testid="stImage"] {
            margin-left: -1.2rem !important; 
            margin-right: -1.2rem !important; 
            width: calc(100% + 2.4rem) !important; 
            max-width: none !important;
            padding: 0 !important;
        }

        [data-testid="stSidebar"] [data-testid="stImage"] img {
            border-radius: 0px !important; 
            width: 100% !important;
        }

        div[data-testid="stDialog"] div[role="dialog"] {
            width: 80vw !important;
            max-width: 80vw !important;
            height: 90vh !important;
            max-height: 90vh !important;
            display: flex;
            flex-direction: column;
            justify-content: space-evenly;
        }

        div[data-testid="stDialog"] [data-testid="stHorizontalBlock"] {
            margin-top: auto !important;
            margin-bottom: auto !important;
        }
    </style>
""", unsafe_allow_html=True)

initialize_states()

with st.sidebar:
    col_up, col_res = st.columns(2, vertical_alignment="bottom")
    
    with col_up:
        file = st.file_uploader("Upload", label_visibility="collapsed")

    if file:
        img = np.array(Image.open(file).convert("L"))
        if (st.session_state.uploaded_img is None):
            st.session_state.uploaded_img = img.copy()
            st.session_state.working_img = img.copy()
            st.session_state.history = [{"image": img.copy(), "title": "Original"}]

    with col_res:
        has_operations = False
        if st.session_state.uploaded_img is not None:
            has_operations = len(st.session_state.history) > 1
        
        if st.button("Reset", disabled=not has_operations, use_container_width=True):
            reset_operation()

    st.write("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    category = st.selectbox("Category", list(OPERATIONS.keys()))
    operation = st.selectbox("Operation", list(OPERATIONS[category].keys()))
    config = OPERATIONS[category][operation]

    preview, hist_title = build_ui(st.session_state.working_img, config)

    st.write("<div style='height: 5px;'></div>", unsafe_allow_html=True) 
    col_app, col_hist = st.columns([2, 2], vertical_alignment="bottom") 
    
    with col_app:
        if st.button("Apply", type="primary", use_container_width=True):
            if preview is not None:
                apply_operation(preview, hist_title)
                
    with col_hist:
        if st.button("History", use_container_width=True): # Fixed indentation here
            show_history_modal()

    st.write("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    render_sidebar_plot(category, operation, st.session_state.working_img, preview)

st.markdown("""
    <div class='topbar'>
        <div class='topbar-title'>
            Digital Image Processing Playground
        </div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.preview is not None:
    show_main_images()
    render_main_plot(category, st.session_state.working_img, st.session_state.preview)

components.html(
    """
        <script>
            const doc = window.parent.document;
            const scrollContainer = doc.querySelector('[data-testid="stMain"]');
            
            function updateOpacity() {
                const tb = doc.querySelector('.topbar');
                if (tb && scrollContainer) {
                    tb.style.opacity = scrollContainer.scrollTop > 50 ? '0' : '1';
                }
            }

            updateOpacity();

            if (scrollContainer) {
                scrollContainer.addEventListener('scroll', updateOpacity, { passive: true });
            }

            let checks = 0;
            let interval = setInterval(() => {
                updateOpacity();
                checks++;
                if (checks > 20) clearInterval(interval); 
            }, 100);
        </script>
    """, height=0, width=0
)