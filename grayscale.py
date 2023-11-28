import cv2
import numpy as np

def generate_pseudorandom_pattern(image_shape, seed, k):
    # Menghasilkan pola pseudorandom menggunakan LCG (Linear Congruential Generator)
    np.random.seed(seed)
    pattern = np.random.randint(0, 256, size=image_shape, dtype=np.uint8)
    pattern = k * pattern
    return pattern

def watermark_image(image, watermark_pattern):
    # Menambahkan watermark pada citra grayscale
    watermarked_image = cv2.addWeighted(image, 1, watermark_pattern, 1, 0, dtype=cv2.CV_8U)
    return watermarked_image

def main():
    # Baca citra grayscale
    image = cv2.imread('mcqueen.jpeg', cv2.IMREAD_GRAYSCALE)

    # Tentukan seed dan bobot pengali (k)
    seed = 42
    k = 100

    # Generate pseudorandom pattern
    watermark_pattern = generate_pseudorandom_pattern(image.shape, seed, k)

    # Tambahkan watermark pada citra
    watermarked_image = watermark_image(image, watermark_pattern)

    # Simpan citra hasil watermarking
    cv2.imwrite('watermarked_image.jpg', watermarked_image)

    cv2.imshow('Original Image', image)
    cv2.imshow('Watermarked Image', watermarked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
