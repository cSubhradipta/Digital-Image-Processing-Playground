import streamlit as st #type: ignore
import matplotlib.pyplot as plt
import numpy as np

def initialize_states():
    defaults = {
        "uploaded_img": None,
        "working_img": None,
        "history": [],
        "preview": None,
        "carousel_idx": 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_operation():
    if st.session_state.uploaded_img is not None:
        st.session_state.working_img = st.session_state.uploaded_img.copy()
        st.session_state.preview = st.session_state.uploaded_img.copy()
        st.session_state.history = [{
            "image": st.session_state.uploaded_img.copy(),
            "title": "Original"
        }]
        st.session_state.carousel_idx = 0
        st.rerun()

def prev_hist():
    st.session_state.carousel_idx -= 1

def next_hist():
    st.session_state.carousel_idx += 1

def apply_operation(preview, title):
    st.session_state.history.append({
        "image": preview.copy(),
        "title": title
    })
    st.session_state.working_img = preview.copy()
    
    n = len(st.session_state.history)
    if n > 3:
        st.session_state.carousel_idx = n - 3
        
    st.rerun()

def get_fourier_spectrum(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    return magnitude_spectrum

def build_ui(img, config):
    if img is None: return None, ""
    if config["type"] == "slider":
        value = st.slider(config["slider_label"], config["min"], config["max"], config["default"], key=config["key"])
        if isinstance(value, tuple):
            preview = config["func"](img, value[0], value[1])
            st.session_state.preview = preview
            return preview, config["history"].format(value[0], value[1])
        else:
            preview = config["func"](img, value)
            st.session_state.preview = preview
            return preview, config["history"].format(value)
    else:
        preview = config["func"](img)
        st.session_state.preview = preview
        return preview, config["history"]


def show_main_images():
    with st.container():
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            st.image(st.session_state.working_img, caption="Current", use_container_width=True)
        with col2:
            st.image(st.session_state.preview, caption="Preview", use_container_width=True)


@st.dialog("Processing Timeline", width="large")
def show_history_modal():
    history = st.session_state.history
    n = len(history)

    if n == 0:
        st.info("No history available")
        return

    idx = max(0, min(st.session_state.carousel_idx, n - 3 if n > 2 else 0))
    
    nav_left, img_col1, img_col2, img_col3, nav_right = st.columns([0.5, 3, 3, 3, 0.5], vertical_alignment="center")

    with nav_left:
        st.button("◀", disabled=(idx <= 0), use_container_width=True, key="prev_hist_modal", on_click=prev_hist)

    with img_col1:
        st.image(history[idx]["image"], use_container_width=True)
        st.markdown(f"<p style='text-align: center; font-weight:bold; font-size:14px; margin-top:5px;'>{history[idx]['title']}</p>", unsafe_allow_html=True)

    with img_col2:
        if idx + 1 < n:
            st.image(history[idx+1]["image"], use_container_width=True)
            st.markdown(f"<p style='text-align: center; font-weight:bold; font-size:14px; margin-top:5px; color:#4DA3FF;'>{history[idx+1]['title']}</p>", unsafe_allow_html=True)

    with img_col3:
        if idx + 2 < n:
            st.image(history[idx+2]["image"], use_container_width=True)
            st.markdown(f"<p style='text-align: center; font-weight:bold; font-size:14px; margin-top:5px; color:#FF5733;'>{history[idx+2]['title']}</p>", unsafe_allow_html=True)

    with nav_right:
        st.button("▶", disabled=(idx >= n - 3), use_container_width=True, key="next_hist_modal", on_click=next_hist)


def apply_plot_theme(fig, ax):
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    theme_color = "#e5e7eb" 
    
    ax.tick_params(axis='both', which='major', labelsize=10, colors=theme_color, width=1.0, length=5)
    
    for spine in ax.spines.values():
        spine.set_color(theme_color)
        spine.set_linewidth(1.0) 
        
    ax.title.set_color(theme_color)
    ax.title.set_fontweight("normal")
    ax.title.set_fontsize(13)
    ax.xaxis.label.set_color(theme_color)
    ax.xaxis.label.set_fontsize(11)
    ax.yaxis.label.set_color(theme_color)
    ax.yaxis.label.set_fontsize(11)

    if ax.axison:
        ax.grid(True, color=theme_color, alpha=0.15, linestyle='--', linewidth=0.5)


def render_sidebar_plot(category, operation, original, preview):
    if preview is None or category == "Histogram Equalization":
        return

    if category == "Noise Generation":
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        ax.hist(preview.ravel(), bins=256, range=(0, 256), color='#4DA3FF', alpha=0.7, density=True)
        ax.set_title("Noisy Histogram", pad=10)
        ax.set_xlim([-5, 260])
        ax.set_yticks([])
        apply_plot_theme(fig, ax)
        fig.tight_layout(pad=0.5)
        st.pyplot(fig, transparent=True, use_container_width=True)

    elif operation == "Gamma Transform":
        gamma = st.session_state.get("gamma", 1.0)
        x = np.linspace(0, 1, 256)
        y = np.power(x, gamma)

        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        ax.plot(x, y, color='#4DA3FF', linewidth=2) 
        ax.set_title(f"Gamma ={gamma:.2f}", pad=10)
        
        apply_plot_theme(fig, ax)
        fig.tight_layout(pad=0.5)
        st.pyplot(fig, transparent=True, use_container_width=True)
        
    elif operation == "Thresholding":
        thresh = st.session_state.get("threshold", 128)
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        
        if original is not None:
            ax.hist(original.ravel(), bins=256, range=(0, 256), color='#4DA3FF', alpha=0.7, density=True, zorder=1)
        
        ax.axvspan(-5, thresh, color='#111827', alpha=0.75, zorder=2)
        ax.axvline(x=thresh, color='#FF4B4B', linewidth=2.5, linestyle='--', zorder=3)
        
        ax.set_title(f"Threshold (T={thresh})", pad=10)
        ax.set_xlim([-5, 260])
        ax.set_yticks([]) 
        
        apply_plot_theme(fig, ax)
        fig.tight_layout(pad=0.5) 
        st.pyplot(fig, transparent=True, use_container_width=True)

    elif operation == "Gray Level Slicing":
        val = st.session_state.get("gray_slice", (100, 150))
        low, high = val if isinstance(val, tuple) else (100, 150)
        
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        if original is not None:
            ax.hist(original.ravel(), bins=256, range=(0, 256), color='#4DA3FF', alpha=0.7, density=True, zorder=1)
        
        ax.axvspan(-5, low, color='#111827', alpha=0.85, zorder=2)
        ax.axvspan(high, 260, color='#111827', alpha=0.85, zorder=2)
        
        ax.axvline(x=low, color='#FF4B4B', linewidth=2.5, linestyle='--', zorder=3)
        ax.axvline(x=high, color='#FF4B4B', linewidth=2.5, linestyle='--', zorder=3)
        
        ax.set_title(f"Range: [{low}, {high}]", pad=10)
        ax.set_xlim([-5, 260])
        ax.set_yticks([]) 
        
        apply_plot_theme(fig, ax)
        fig.tight_layout(pad=0.5) 
        st.pyplot(fig, transparent=True, use_container_width=True)

    elif operation == "Logarithmic Transform":
        x = np.linspace(0, 255, 256)
        c = 255 / np.log(1 + 255)
        y = c * np.log(1 + x)
        
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        ax.plot(x, y, color='#4DA3FF', linewidth=2.5) 
        ax.set_title("Logarithmic Curve", pad=10)
        
        ax.set_xlim([-5, 260])
        ax.set_ylim([-5, 260])
        
        apply_plot_theme(fig, ax)
        fig.tight_layout(pad=0.5)
        st.pyplot(fig, transparent=True, use_container_width=True)


def render_main_plot(category, original, preview):
    if preview is None:
        return

    if category == "Histogram Equalization":
        st.write("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(9, 6)) 
            ax.hist(original.ravel(), bins=256, range=(0, 256), color='#4DA3FF', alpha=0.8)
            ax.set_title("Original Histogram", pad=15)
            ax.set_xlim([-5, 260])
            apply_plot_theme(fig, ax)
            fig.tight_layout(pad=1.0)
            st.pyplot(fig, transparent=True, use_container_width=True)

        with col2:
            fig, ax = plt.subplots(figsize=(9, 6)) 
            ax.hist(preview.ravel(), bins=256, range=(0, 256), color='#4DA3FF', alpha=0.8)
            ax.set_title("Equalized Histogram", pad=15)
            ax.set_xlim([-5, 260])
            apply_plot_theme(fig, ax)
            fig.tight_layout(pad=1.0)
            st.pyplot(fig, transparent=True, use_container_width=True)

    elif category == "Noise Generation":
        st.write("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(9, 6)) 
            ax.imshow(get_fourier_spectrum(original), cmap='gray')
            ax.set_title("Original Frequency Spectrum", pad=15)
            ax.axis('off')
            apply_plot_theme(fig, ax)
            fig.tight_layout(pad=1.0)
            st.pyplot(fig, transparent=True, use_container_width=True)

        with col2:
            fig, ax = plt.subplots(figsize=(9, 6)) 
            ax.imshow(get_fourier_spectrum(preview), cmap='gray')
            ax.set_title("Noisy Frequency Spectrum", pad=15)
            ax.axis('off')
            apply_plot_theme(fig, ax)
            fig.tight_layout(pad=1.0)
            st.pyplot(fig, transparent=True, use_container_width=True)

    elif category == "Frequency Domain":
        st.write("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        show_boundary = st.checkbox("Show Filter Boundary", value=True)
        st.write("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        rows, cols = original.shape
        crow, ccol = rows // 2, cols // 2
        cutoff = st.session_state.get('freq_cutoff', 50)
        
        def draw_rings(ax):
            if isinstance(cutoff, tuple):
                ax.add_patch(plt.Circle((ccol, crow), cutoff[0], color='#FF4B4B', fill=False, linestyle='--', linewidth=2))
                ax.add_patch(plt.Circle((ccol, crow), cutoff[1], color='#FF4B4B', fill=False, linestyle='--', linewidth=2))
            else:
                ax.add_patch(plt.Circle((ccol, crow), cutoff, color='#FF4B4B', fill=False, linestyle='--', linewidth=2))

        with col1:
            fig, ax = plt.subplots(figsize=(9, 6)) 
            ax.imshow(get_fourier_spectrum(original), cmap='gray')
            ax.set_title("Original Spectrum", pad=15)
            ax.axis('off')
            
            if show_boundary:
                draw_rings(ax)
                
            apply_plot_theme(fig, ax)
            fig.tight_layout(pad=1.0)
            st.pyplot(fig, transparent=True, use_container_width=True)

        with col2:
            fig, ax = plt.subplots(figsize=(9, 6)) 
            ax.imshow(get_fourier_spectrum(preview), cmap='gray')
            ax.set_title("Filtered Spectrum", pad=15)
            ax.axis('off')
                        
            apply_plot_theme(fig, ax)
            fig.tight_layout(pad=1.0)
            st.pyplot(fig, transparent=True, use_container_width=True)