# processor.py
import os
import shutil
from PIL import Image
from .transformations import ColorTransformer
from .resizer import ImageResizer

class ImageProcessor:
    def __init__(self, input_folder, output_folder,
                 color_transformer=None,
                 resizer=None):
        """
        :param input_folder: Directory containing input PNGs.
        :param output_folder: Directory where output images will be saved.
        :param color_transformer: An instance of ColorTransformer (optional).
        :param resizer: An instance of ImageResizer (optional).
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.color_transformer = color_transformer
        self.resizer = resizer
        
        # Ensure the output folder exists.
        os.makedirs(self.output_folder, exist_ok=True)

    def process_all(self, dpi=None):
        """
        Process all .png files in the input folder.
        Apply the color transformation (if configured), then resize (if configured),
        while saving the output images with the specified DPI.
        
        :param dpi: A tuple (x_dpi, y_dpi) to set the image DPI (optional).
        """
        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(".png"):
                input_path = os.path.join(self.input_folder, filename)
                temp_path = None
                
                # Step 1: Transform colors if a color transformer is provided.
                if self.color_transformer:
                    temp_path = os.path.join(self.output_folder, f"temp_{filename}")
                    self.color_transformer.transform(input_path, temp_path, dpi=dpi)
                    input_for_resizing = temp_path
                else:
                    input_for_resizing = input_path
                
                # Step 2: Resize if a resizer is provided.
                if self.resizer:
                    output_path = os.path.join(self.output_folder, filename)
                    self.resizer.resize(input_for_resizing, output_path, dpi=dpi)
                else:
                    # If only color transformation was done, rename the temporary file.
                    final_path = os.path.join(self.output_folder, filename)
                    if self.color_transformer:
                        os.replace(input_for_resizing, final_path)
                    else:
                        # If no processing is configured, copy the file.
                        shutil.copy(input_path, final_path)
                
                # Delete the temporary file if it exists.
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
                
                print(f"Processed: {filename}")
