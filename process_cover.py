import numpy as np
from PIL import Image
import io

def preprocess_image(image: Image.Image, w: int, h: int, resample=Image.NEAREST) -> Image.Image:
    image.copy()

    image.thumbnail((w, h), resample=resample)
    if image.width == w and image.height == h:
        return image
    else:
        avg_color = get_average_color(image)
        padded_img = Image.new("RGBA", (w, h), avg_color)
        paste_position = ((w-image.width)//2, (h-image.height)//2)
        padded_img.paste(image, paste_position)
        return padded_img

def resize_image_for_cover(image: Image.Image) -> Image.Image:
    # Open the image from the bytes
    img = image.copy()
    img = preprocess_image(img, 32, 18)
    img = preprocess_image(img, 16, 16)
    return img

def get_average_color(img: Image) -> tuple:
    # Convert the image to RGB if it's not already
    img = img.convert("RGB")
    
    # Get the image pixels
    pixels = list(img.getdata())
    
    # Calculate the average color
    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)
    
    return (r, g, b, 255)  # Return the color as RGBA (with full alpha)

def process_template(template_bytes: bytes, thumb_data: bytes) -> bytes:
        # Open the template image
        template_img = Image.open(io.BytesIO(template_bytes))
        img_data = template_img.convert("RGBA")

        # Modify the image data according to the thumb_data
        pixels = img_data.load()
        for y in range(16):
            for x in range(16):
                r, g, b, a = pixels[x, y]
                # Check if the pixel is pure green (0, 255, 0) and not transparent
                if r == 0 and g == 255 and b == 0 and a != 0:
                    # Replace green with the thumb data
                    thumb_idx = (y * 16 + x) * 4
                    thumb_pixel = (thumb_data[thumb_idx], thumb_data[thumb_idx+1], thumb_data[thumb_idx+2], thumb_data[thumb_idx+3])
                    pixels[x, y] = thumb_pixel
        
        # Save the modified image back to bytes
        with io.BytesIO() as output:
            img_data.save(output, format="PNG")
            return output.getvalue()

def adapt_image_to_disc(image: bytes, fragment_template: bytes, disc_template: bytes) -> dict:
    # Get the thumb data
    thumb_data = resize_image_for_cover(Image.open(io.BytesIO(image))).tobytes()

    # Process both the fragment and disc textures
    fragment_texture = process_template(fragment_template, thumb_data)
    disc_texture = process_template(disc_template, thumb_data)

    return {
        'discTexture': disc_texture,
        'fragmentTexture': fragment_texture
    }

def save_textures(result: dict, disc_path: str, fragment_path: str) -> None:
    # Save the disc texture to a file
    with open(disc_path, "wb") as f:
        f.write(result['discTexture'])

    # Save the fragment texture to a file
    with open(fragment_path, "wb") as f:
        f.write(result['fragmentTexture'])

if __name__ == '__main__':
    with open("maxresdefault.jpg", "rb") as f:
        image_bytes = f.read()

    with open("fragment_template.webp", "rb") as f:
        fragment_template_bytes = f.read()

    with open("disc_template.webp", "rb") as f:
        disc_template_bytes = f.read()

    result = adapt_image_to_disc(image_bytes, fragment_template_bytes, disc_template_bytes)
    save_textures(result, "disc_texture.png", "fragment_texture.png")