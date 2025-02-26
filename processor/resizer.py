# resizer.py
from PIL import Image

class ImageResizer:
    def __init__(self, width=None, height=None, keep_aspect_ratio=True):
        """
        :param width:  Desired width in pixels (int) or None
        :param height: Desired height in pixels (int) or None
        :param keep_aspect_ratio: bool, whether to maintain the original aspect ratio
        """
        self.width = width
        self.height = height
        self.keep_aspect_ratio = keep_aspect_ratio

    def resize(self, image_path: str, output_path: str, dpi: tuple[int, int] | None = None) -> None:
        """
        Open an image, resize it, then save with an optional DPI setting.
        
        :param image_path: Path to the input image.
        :param output_path: Path to save the resized image.
        :param dpi: A tuple (x_dpi, y_dpi) to set the image DPI.
        """
        img = Image.open(image_path)
        original_width, original_height = img.size

        if not self.keep_aspect_ratio and self.width and self.height:
            new_width = self.width
            new_height = self.height
        else:
            if self.width and not self.height:
                aspect_ratio = original_height / original_width
                new_width = self.width
                new_height = int(new_width * aspect_ratio)
            elif self.height and not self.width:
                aspect_ratio = original_width / original_height
                new_height = self.height
                new_width = int(new_height * aspect_ratio)
            else:
                new_width = self.width if self.width else original_width
                new_height = self.height if self.height else original_height

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        if dpi:
            resized_img.save(output_path, dpi=dpi)
        else:
            resized_img.save(output_path)
