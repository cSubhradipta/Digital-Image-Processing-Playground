import numpy as np
import matplotlib.pyplot as plt

def histogram_equalization(img):
    hist = np.zeros(256)

    for val in img.flatten():
        hist[val] += 1

    pdf = hist / img.size
    cdf = np.cumsum(pdf)
    new_vals = np.floor(255 * cdf).astype(np.uint8)
    out = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out[i, j] = new_vals[img[i, j]]
    return out

def plot_histogram(img):
    fig, ax = plt.subplots()
    ax.hist(
        img.ravel(),
        bins=256,
        range=(0,256)
    )
    return fig