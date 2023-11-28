import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class WatermarkingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Watermarking Tool")

        self.k_label = tk.Label(master, text="K Value:")
        self.k_label.pack()

        self.k_slider = tk.Scale(master, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200)
        self.k_slider.set(0.1)
        self.k_slider.pack()

        self.open_button = tk.Button(master, text="Open Image", command=self.open_image)
        self.open_button.pack()

        self.generate_button = tk.Button(master, text="Generate Watermarked Image", command=self.generate_watermarked_image)
        self.generate_button.pack()

        self.original_image_tk = None
        self.watermarked_image_tk = None

        self.original_image_label = tk.Label(master)
        self.original_image_label.pack(side=tk.LEFT)

        self.watermarked_image_label = tk.Label(master)
        self.watermarked_image_label.pack(side=tk.RIGHT)

        self.original_caption_label = tk.Label(master, text="Original Image")
        self.original_caption_label.pack(side=tk.LEFT)

        self.watermarked_caption_label = tk.Label(master, text="Watermarked Image")
        self.watermarked_caption_label.pack(side=tk.RIGHT)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.original_image = image  
            image = Image.fromarray(image)
            self.original_image_tk = ImageTk.PhotoImage(image)
            self.original_image_label.config(image=self.original_image_tk)
            self.original_image_label.image = self.original_image_tk
            self.original_caption_label.config(text="Original Image")

    def generate_watermarked_image(self):
        if not hasattr(self, 'original_image'):
            messagebox.showerror("Error", "Please open an image first.")
            return

        k_value = self.k_slider.get()
        seed = 42 

        watermark_pattern = self.generate_pseudorandom_pattern(self.original_image.shape, seed, k_value)
        watermarked_image = self.watermark_image(self.original_image, watermark_pattern)

        cv2.imwrite('watermarked_image.jpg', watermarked_image)

        image = Image.fromarray(watermarked_image)
        self.watermarked_image_tk = ImageTk.PhotoImage(image)

        self.watermarked_image_label.config(image=self.watermarked_image_tk)
        self.watermarked_image_label.image = self.watermarked_image_tk
        self.watermarked_caption_label.config(text="Watermarked Image")

        messagebox.showinfo("Success", "Watermarked image saved as 'watermarked_image.jpg'")

    @staticmethod
    def generate_pseudorandom_pattern(image_shape, seed, k):
        np.random.seed(seed)
        pattern = np.random.randint(0, 256, size=image_shape, dtype=np.uint8)
        pattern = k * pattern
        return pattern

    @staticmethod
    def watermark_image(image, watermark_pattern):
        watermarked_image = cv2.addWeighted(image, 1, watermark_pattern, 1, 0, dtype=cv2.CV_8U)
        return watermarked_image

def main():
    root = tk.Tk()
    app = WatermarkingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
