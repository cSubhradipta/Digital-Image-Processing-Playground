def quantize(img, bits):
    levels = 2 ** bits
    factor = 256 // levels
    return (img // factor) * factor


def downsample(img, factor):
    return img[::factor, ::factor]