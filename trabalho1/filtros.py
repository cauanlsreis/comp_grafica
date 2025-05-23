# Importações
from PIL import Image, ImageFilter, ImageChops
import numpy as np
import random
import math

# Filtro Negativo
def filtro_negativo(img):
    img = img.convert('RGB')
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (255 - r, 255 - g, 255 - b)
    return img

# Filtro Escala de Cinza
def filtro_escala_cinza(img):
    img = img.convert("RGB")
    matriz = img.load()
    largura, altura = img.size

    for i in range(largura):
        for j in range(altura):
            r, g, b = matriz[i, j]
            media = (r + g + b) // 3
            matriz[i, j] = (media, media, media)
    return img


# Filtro Gama
def filtro_gama(img, fator=2.2):
    img = img.convert('RGB')
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                int((r / 255) ** fator * 255),
                int((g / 255) ** fator * 255),
                int((b / 255) ** fator * 255)
            )
    return img

# Filtro Logarítmico
def filtro_logaritmo(img):
    img = img.convert('RGB')
    pixels = img.load()
    c = 255 / math.log(256)
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                int(c * math.log(1 + r)),
                int(c * math.log(1 + g)),
                int(c * math.log(1 + b))
            )
    return img

# Filtro Preto e Branco
def filtro_pb(img):
    img = img.convert('RGB')
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            media = (r + g + b) // 3
            cor = (0, 0, 0) if media < 128 else (255, 255, 255)
            pixels[i, j] = cor
    return img

# Filtro Blur
def filtro_blur(img):
    kernel = ImageFilter.Kernel(
        size=(3, 3),
        kernel=(1, 1, 1, 1, 1, 1, 1, 1, 1),
        scale=9,
        offset=0
    )
    return img.filter(kernel)

# Filtro Sharpen (Nitidez)
def filtro_sharpen(img):
    kernel = ImageFilter.Kernel(
        size=(3, 3),
        kernel=(0, -1, 0, -1, 5, -1, 0, -1, 0),
        scale=1,
        offset=0
    )
    return img.filter(kernel)

# Filtro Contorno
def filtro_contorno(img):
    kernel = ImageFilter.Kernel(
        size=(3, 3),
        kernel=(-1, -1, -1, -1, 8, -1, -1, -1, -1),
        scale=1,
        offset=0
    )
    return img.filter(kernel)

# Filtro Sobel
def filtro_sobel(img):
    img = img.convert('L')
    sobel_x = ImageFilter.Kernel((3, 3), (-1, 0, 1, -2, 0, 2, -1, 0, 1), scale=1)
    sobel_y = ImageFilter.Kernel((3, 3), (-1, -2, -1, 0, 0, 0, 1, 2, 1), scale=1)
    img_x = img.filter(sobel_x)
    img_y = img.filter(sobel_y)
    return ImageChops.add(img_x, img_y)

# Filtro Laplaciano
def filtro_laplaciano(img):
    img = img.convert('L')
    kernel = ImageFilter.Kernel(
        (3, 3),
        (1, 1, 1, 1, -8, 1, 1, 1, 1),
        scale=1,
        offset=0
    )
    return img.filter(kernel)

# Filtro Piwwit
def filtro_piwwit(img):
    img = img.convert('L')
    kernel_x = ImageFilter.Kernel((3, 3), (-1, 0, 1, -1, 0, 1, -1, 0, 1), scale=1)
    kernel_y = ImageFilter.Kernel((3, 3), (-1, -1, -1, 0, 0, 0, 1, 1, 1), scale=1)
    img_x = img.filter(kernel_x)
    img_y = img.filter(kernel_y)
    return ImageChops.add(img_x, img_y)

# Filtro de Ruído (sal e pimenta)
def filtro_ruido(img, prob=0.06):
    img = img.convert("RGB")
    np_img = np.array(img)

    for i in range(np_img.shape[0]):
        for j in range(np_img.shape[1]):
            rand = random.random()
            if rand < prob:
                np_img[i, j] = [0, 0, 0]  # Preto
            elif rand > 1 - prob:
                np_img[i, j] = [255, 255, 255]  # Branco

    return Image.fromarray(np_img)