import numpy as np

def negative(img):
    return 255 - img


def threshold(img, T):
    out = np.zeros_like(img)
    out[img > T] = 255
    return out


def log_transform(img):
    img = img / 255.0
    out = np.log(1 + img)
    out = out / out.max()
    return (out * 255).astype(np.uint8)


def gamma_transform(img, gamma):
    img = img / 255.0
    out = np.power(img, gamma)
    return (out * 255).astype(np.uint8)


def gray_slice(img, low, high):
    out = np.zeros_like(img)
    mask = (img >= low) & (img <= high)
    out[mask] = 255
    return out


def bit_plane(img, bit):
    return ((img >> bit) & 1) * 255