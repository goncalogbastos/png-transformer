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
        :param input_folder: Directory containing input PNGs (and possibly subfolders like 16, 32).
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
        Walk through all subdirectories in self.input_folder and process .png files.
        If subfolder is named '16', '32', etc., we set that as the width to resize.
        Output is always saved in self.output_folder.
        
        :param dpi: A tuple (x_dpi, y_dpi) to set the image DPI (optional).
        """
        # Walk through input folder, subfolders, and files
        for root, dirs, files in os.walk(self.input_folder):
            for filename in files:
                if filename.lower().endswith(".png"):
                    # Full path to the current input PNG
                    input_path = os.path.join(root, filename)
                    
                    # Figure out subfolder name (e.g., "16", "32", etc.)
                    subfolder_name = os.path.basename(root)
                    
                    # Try to parse the subfolder name as an integer (size)
                    if self.resizer:
                        try:
                            size = int(subfolder_name)
                            self.resizer.width = size
                        except ValueError:
                            # If the folder name isn't a number, default to 32 or some fallback
                            self.resizer.width = 32

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
