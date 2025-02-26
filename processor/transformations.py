# transformations.py
import numpy as np
from PIL import Image

class ColorTransformer:
    def __init__(self,
                 white_threshold=240,
                 black_threshold=15,
                 dark_gray=(40, 40, 40),
                 white=(255, 255, 255)):
        """
        :param white_threshold: int, threshold above which a pixel is considered 'nearly white'
        :param black_threshold: int, threshold below which a pixel is considered 'nearly black'
        :param dark_gray: tuple(R, G, B), color to apply to nearly white pixels
        :param white: tuple(R, G, B), color to apply to nearly black pixels
        """
        self.white_threshold = white_threshold
        self.black_threshold = black_threshold
        self.dark_gray = dark_gray
        self.white = white

    def transform(self, image_path, output_path, dpi=None):
        """
        Open an image, transform nearly white pixels to dark gray and nearly black pixels to white,
        then save the image with an optional DPI setting.
        
        :param image_path: Path to the input image.
        :param output_path: Path to save the transformed image.
        :param dpi: A tuple (x_dpi, y_dpi) to set the image DPI (e.g., (300,300)).
        """
        img = Image.open(image_path).convert("RGBA")
        data = np.array(img)

        # Create masks for nearly white and nearly black pixels.
        nearly_white_mask = (
            (data[:, :, 0] >= self.white_threshold) &
            (data[:, :, 1] >= self.white_threshold) &
            (data[:, :, 2] >= self.white_threshold)
        )
        nearly_black_mask = (
            (data[:, :, 0] <= self.black_threshold) &
            (data[:, :, 1] <= self.black_threshold) &
            (data[:, :, 2] <= self.black_threshold)
        )

        # Apply color transformations.
        data[nearly_white_mask, :3] = self.dark_gray
        data[nearly_black_mask, :3] = self.white

        # Convert array back to image.
        new_img = Image.fromarray(data, mode="RGBA")
        # Save with the specified dpi if provided.
        if dpi:
            new_img.save(output_path, dpi=dpi)
        else:
            new_img.save(output_path)
