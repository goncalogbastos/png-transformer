# main.py
from processor import ColorTransformer, ImageResizer, ImageProcessor

WHITE_THRESHOLD = 240
BLACK_THRESHOLD = 15
DARK_GRAY = 117
WHITE = 255
DPI = 96

transformer = ColorTransformer(
    white_threshold=WHITE_THRESHOLD,
    black_threshold=BLACK_THRESHOLD,
    dark_gray=(DARK_GRAY, DARK_GRAY, DARK_GRAY),
    white=(WHITE, WHITE, WHITE)
)

# Set width=None here; we'll pick the actual size dynamically in processor.py
resizer = ImageResizer(width=None, height=None, keep_aspect_ratio=True)

processor = ImageProcessor(
    input_folder="input",
    output_folder="output",
    color_transformer=transformer,
    resizer=resizer,
)

# Process all images with the specified DPI
processor.process_all(dpi=(DPI, DPI))
