from pillow import Image
import numpy as np

def get_image_data(image_path: str) -> np.ndarray:
    # Open the image using Pillow
    img = Image.open(image_path)
    
    # Resize the image to 16x16
    img_resized = img.resize((16, 16))
    
    # Convert the image to RGBA format
    img_resized_rgba = img_resized.convert('RGBA')
    
    # Convert the image to a NumPy array and flatten it
    img_data = np.array(img_resized_rgba)
    
    # Flatten the image data (similar to Uint8ClampedArray in JavaScript)
    return img_data.flatten()

def save_as_bmp(image_data: np.ndarray, output_path: str):
    # Reshape the flattened array back to a 16x16 image with 4 channels (RGBA)
    img_reshaped = image_data.reshape((16, 16, 4))

    # Create a Pillow image from the NumPy array (RGBA format)
    img_pil = Image.fromarray(img_reshaped, 'RGBA')

    # Save the image as a BMP file
    img_pil.save(output_path, 'BMP')

# Example usage:
image_data = get_image_data('path_to_image.jpg')
save_as_bmp(image_data, 'output_image.bmp')
