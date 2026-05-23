from operations.point_processing import *
from operations.filters import *
from operations.histogram_equalization import *
from operations.resolution import *
from operations.noise import *
from operations.frequency import *

OPERATIONS = {
    "Point Processing": {
        "Negative": {
            "type": "normal",
            "func": negative,
            "history": "Negative",
            "key": "negative"
        },
        "Gamma Transform": {
            "type": "slider",
            "func": gamma_transform,
            "slider_label": "Gamma",
            "min": 0.1,
            "max": 5.0,
            "default": 1.0,
            "history": "Gamma = {:.2f}",
            "key": "gamma"
        },
        "Logarithmic Transform": {
            "type": "normal",
            "func": log_transform,
            "history": "Log Transform",
            "key": "log_transform"
        },
        "Thresholding": {
            "type": "slider",
            "func": threshold,
            "slider_label": "Threshold Value",
            "min": 0,
            "max": 255,
            "default": 128,
            "history": "Threshold (T={})",
            "key": "threshold"
        },
        "Gray Level Slicing": {
            "type": "slider",
            "func": gray_slice,
            "slider_label": "Intensity Span",
            "min": 0,
            "max": 255,
            "default": (100, 150), 
            "history": "Gray Slice ({}-{})",
            "key": "gray_slice"
        }
    },
    
    "Filters (Spatial Domain)": {
        "Mean Filter (Blur)": {
            "type": "slider",
            "func": avg_filter,
            "slider_label": "Kernel Size (k x k)",
            "min": 3,
            "max": 21,
            "default": 3,
            "history": "Mean Filter (k={})",
            "key": "mean_filter"
        },
        "Median Filter": {
            "type": "slider",
            "func": median_filter,
            "slider_label": "Kernel Size",
            "min": 3,
            "max": 21,
            "default": 3,
            "history": "Median Filter (k={})",
            "key": "median_filter"
        },
        "Sobel Edge Detection": {
            "type": "normal",
            "func": sobel,
            "history": "Sobel Edges",
            "key": "sobel"
        },
        "Laplacian": {
            "type": "normal",
            "func": laplacian,
            "history": "Laplacian",
            "key": "laplacian"
        }
    },

    "Histogram Equalization": {
        "Global Equalization": {
            "type": "normal",
            "func": histogram_equalization,
            "history": "Global Hist. Eq.",
            "key": "global_hist_eq"
        }
    },

    "Resolution & Sampling": {
        "Spatial Resolution (Pixelate)": {
            "type": "slider",
            "func": downsample,
            "slider_label": "Downsample Step (Nth pixel)",
            "min": 1,
            "max": 20,
            "default": 1,
            "history": "Downsample (Step={})",
            "key": "spatial_res"
        },
        "Intensity Resolution (Quantize)": {
            "type": "slider",
            "func": quantize,
            "slider_label": "Bit Depth",
            "min": 1,
            "max": 8,
            "default": 4,
            "history": "Quantize ({} bits)",
            "key": "intensity_res"
        }
    },

    "Noise Generation": {
        "Gaussian Noise": {
            "type": "slider",
            "func": add_gaussian_noise,
            "slider_label": "Variance",
            "min": 0.001,
            "max": 0.1,
            "default": 0.01,
            "history": "Gaussian Noise (v={:.3f})",
            "key": "gaussian_noise"
        },
        "Salt & Pepper Noise": {
            "type": "slider",
            "func": add_salt_pepper_noise,
            "slider_label": "Probability",
            "min": 0.01,
            "max": 0.2,
            "default": 0.05,
            "history": "S&P Noise (p={:.2f})",
            "key": "sp_noise"
        },
        "Periodic Noise": {
            "type": "slider",
            "func": add_periodic_noise,
            "slider_label": "Frequency Intensity",
            "min": 10,
            "max": 100,
            "default": 30,
            "history": "Periodic (f={})",
            "key": "periodic"
        }
    },
    "Frequency Domain": {
        "Ideal Low Pass": {
            "type": "slider", 
            "func": ideal_low_pass, 
            "slider_label": "Cutoff Frequency",
            "min": 1, 
            "max": 300, 
            "default": 50, 
            "history": "ILPF ({})", 
            "key": "ilpf"
        },
        "Butterworth Low Pass": {
            "type": "slider", 
            "func": butterworth_low_pass, 
            "slider_label": "Cutoff Frequency",
            "min": 1, 
            "max": 300, 
            "default": 50, 
            "history": "BLPF ({})", 
            "key": "blpf"
        },
        "Gaussian Low Pass": {
            "type": "slider", 
            "func": gaussian_low_pass, 
            "slider_label": "Cutoff Frequency",
            "min": 1, 
            "max": 300, 
            "default": 50, 
            "history": "GLPF ({})", 
            "key": "glpf"
        },
        "Ideal High Pass": {
            "type": "slider", 
            "func": ideal_high_pass, 
            "slider_label": "Cutoff Frequency",
            "min": 1, 
            "max": 300, 
            "default": 50, 
            "history": "IHPF ({})", 
            "key": "ihpf"
        },
        "Butterworth High Pass": {
            "type": "slider", 
            "func": butterworth_high_pass, 
            "slider_label": "Cutoff Frequency",
            "min": 1, 
            "max": 300, 
            "default": 50, 
            "history": "BHPF ({})", 
            "key": "bhpf"
        },
        "Gaussian High Pass": {
            "type": "slider", 
            "func": gaussian_high_pass, 
            "slider_label": "Cutoff Frequency",
            "min": 1, 
            "max": 300, 
            "default": 50, 
            "history": "GHPF ({})", 
            "key": "ghpf"
        },
        "Ideal Band Reject": {
            "type": "slider", 
            "func": ideal_band_reject, 
            "slider_label": "Frequency Band",
            "min": 1, 
            "max": 300, 
            "default": (30, 70),
            "history": "IBRF ({}-{})", 
            "key": "ibrf"
        },
        "Butterworth Band Reject": {
            "type": "slider", 
            "func": butterworth_band_reject, 
            "slider_label": "Frequency Band",
            "min": 1, 
            "max": 300, 
            "default": (30, 70), 
            "history": "BBRF ({}-{})", 
            "key": "bbrf"
        },
        "Gaussian Band Reject": {
            "type": "slider", 
            "func": gaussian_band_reject, 
            "slider_label": "Frequency Band",
            "min": 1, 
            "max": 300, 
            "default": (30, 70), 
            "history": "GBRF ({}-{})", 
            "key": "gbrf"
        },
        "Ideal Band Pass": {
            "type": "slider", 
            "func": ideal_band_pass, 
            "slider_label": "Frequency Band",
            "min": 1, 
            "max": 300, 
            "default": (30, 70), 
            "history": "IBPF ({}-{})", 
            "key": "ibpf"
        },
        "Butterworth Band Pass": {
            "type": "slider", 
            "func": butterworth_band_pass, 
            "slider_label": "Frequency Band",
            "min": 1, 
            "max": 300, 
            "default": (30, 70), 
            "history": "BBPF ({}-{})", 
            "key": "bbpf"
        },
        "Gaussian Band Pass": {
            "type": "slider", 
            "func": gaussian_band_pass, 
            "slider_label": "Frequency Band",
            "min": 1, 
            "max": 300, 
            "default": (30, 70), 
            "history": "GBPF ({}-{})", 
            "key": "gbpf"
        }
    }
}