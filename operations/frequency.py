import numpy as np
import streamlit as st #type: ignore

def create_distance_matrix(shape):
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    u = np.arange(rows) - crow
    v = np.arange(cols) - ccol
    V, U = np.meshgrid(v, u)
    return np.sqrt(U**2 + V**2)

def apply_freq_filter(image, H, cutoff):
    st.session_state['freq_cutoff'] = cutoff 
    
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    filtered_fshift = fshift * H
    
    f_ishift = np.fft.ifftshift(filtered_fshift)
    img_back = np.fft.ifft2(f_ishift)
    
    return np.clip(np.abs(img_back), 0, 255).astype(np.uint8)

def ideal_low_pass(image, cutoff=50):
    D = create_distance_matrix(image.shape)
    H = np.zeros_like(D)
    H[D <= cutoff] = 1
    return apply_freq_filter(image, H, cutoff)

def butterworth_low_pass(image, cutoff=50):
    n = 2
    D = create_distance_matrix(image.shape)
    H = 1 / (1 + (D / cutoff)**(2 * n))
    return apply_freq_filter(image, H, cutoff)

def gaussian_low_pass(image, cutoff=50):
    D = create_distance_matrix(image.shape)
    H = np.exp(-(D**2) / (2 * (cutoff**2)))
    return apply_freq_filter(image, H, cutoff)


def ideal_high_pass(image, cutoff=50):
    D = create_distance_matrix(image.shape)
    H = np.ones_like(D)
    H[D <= cutoff] = 0
    return apply_freq_filter(image, H, cutoff)

def butterworth_high_pass(image, cutoff=50):
    n = 2
    D = create_distance_matrix(image.shape)
    H = 1 / (1 + (cutoff / (D + 1e-5))**(2 * n))
    return apply_freq_filter(image, H, cutoff)

def gaussian_high_pass(image, cutoff=50):
    D = create_distance_matrix(image.shape)
    H = 1 - np.exp(-(D**2) / (2 * (cutoff**2)))
    return apply_freq_filter(image, H, cutoff)


def ideal_band_reject(image, low=30, high=70):
    D = create_distance_matrix(image.shape)
    H = np.ones_like(D)
    H[(D >= low) & (D <= high)] = 0
    return apply_freq_filter(image, H, (low, high))

def butterworth_band_reject(image, low=30, high=70):
    n = 2
    D0 = (low + high) / 2.0
    W = high - low
    D = create_distance_matrix(image.shape)
    term = (D * W) / (D**2 - D0**2 + 1e-5)
    H = 1 / (1 + term**(2 * n))
    return apply_freq_filter(image, H, (low, high))

def gaussian_band_reject(image, low=30, high=70):
    D0 = (low + high) / 2.0
    W = high - low
    D = create_distance_matrix(image.shape)
    term = ((D**2 - D0**2) / (D * W + 1e-5))**2
    H = 1 - np.exp(-term)
    return apply_freq_filter(image, H, (low, high))


def ideal_band_pass(image, low=30, high=70):
    D = create_distance_matrix(image.shape)
    H = np.zeros_like(D)
    H[(D >= low) & (D <= high)] = 1
    return apply_freq_filter(image, H, (low, high))

def butterworth_band_pass(image, low=30, high=70):
    n = 2
    D0 = (low + high) / 2.0
    W = high - low
    D = create_distance_matrix(image.shape)
    term = (D * W) / (D**2 - D0**2 + 1e-5)
    H = 1 - (1 / (1 + term**(2 * n)))
    return apply_freq_filter(image, H, (low, high))

def gaussian_band_pass(image, low=30, high=70):
    D0 = (low + high) / 2.0
    W = high - low
    D = create_distance_matrix(image.shape)
    term = ((D**2 - D0**2) / (D * W + 1e-5))**2
    H = np.exp(-term)
    return apply_freq_filter(image, H, (low, high))