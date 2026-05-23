import numpy as np

def add_gaussian_noise(image, mean=0, var=0.01):
    image = image / 255.0
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, image.shape)
    noisy = image + gauss
    return np.clip(noisy * 255, 0, 255).astype(np.uint8)

def add_salt_pepper_noise(image, prob=0.05):
    output = np.copy(image)
    
    num_salt = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    output[tuple(coords)] = 255
    
    num_pepper = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    output[tuple(coords)] = 0
    return output

def add_periodic_noise(image, freq_u=30, freq_v=30, amplitude=40):
    rows, cols = image.shape
    x = np.arange(cols)
    y = np.arange(rows)
    X, Y = np.meshgrid(x, y)
    
    noise = amplitude * np.sin(2 * np.pi * ((freq_u * X / cols) + (freq_v * Y / rows)))
    noisy = image + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)