import numpy as np

def convolve(img, kernel, mode="constant"):
    k = kernel.shape[0]
    pad = k // 2
    padded = np.pad(img, pad, mode=mode)
    out = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+k, j:j+k]
            out[i, j] = np.sum(region * kernel)
    return np.clip(out, 0, 255).astype(np.uint8)


def avg_filter(img, k):
    kernel = np.ones((k, k)) / (k * k)
    return convolve(img, kernel)

def weighted_filter(img):
    kernel = np.array([
        [1,2,1],
        [2,4,2],
        [1,2,1]
    ]) / 16
    return convolve(img, kernel)

def median_filter(img, k):
    pad = k // 2
    padded = np.pad(img, pad)
    out = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+k, j:j+k]
            out[i, j] = np.median(region)

    return out

def laplacian(img):
    kernel = np.array([
        [0,1,0],
        [1,-4,1],
        [0,1,0]
    ])
    lap = convolve(img, kernel)
    return np.clip(img - lap, 0, 255).astype(np.uint8)

def sobel(img):
    gx = np.array([
        [-1,0,1],
        [-2,0,2],
        [-1,0,1]
    ])
    gy = np.array([
        [-1,-2,-1],
        [0,0,0],
        [1,2,1]
    ])
    sx = convolve(img, gx)
    sy = convolve(img, gy)
    mag = np.sqrt(sx**2 + sy**2)
    return np.clip(mag, 0, 255).astype(np.uint8)