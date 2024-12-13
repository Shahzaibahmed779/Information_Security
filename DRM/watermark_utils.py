from PIL import Image

def text_to_binary(text):
    """Convert text to a binary string."""
    return ''.join([format(ord(char), '08b') for char in text])

def binary_to_text(binary):
    """Convert a binary string to text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def embed_watermark(input_image_path, output_image_path, watermark_text):
    image = Image.open(input_image_path)

    # Convert to RGB regardless of format
    if image.mode != 'RGB':
        image = image.convert('RGB')

    binary_watermark = text_to_binary(watermark_text)
    binary_length = format(len(binary_watermark), '032b')  # Store length in first 32 bits

    pixels = list(image.getdata())
    new_pixels = []
    data = binary_length + binary_watermark
    data_index = 0
    data_length = len(data)

    for pixel in pixels:
        r, g, b = pixel
        if data_index < data_length:
            r = (r & ~1) | int(data[data_index])
            data_index += 1
        if data_index < data_length:
            g = (g & ~1) | int(data[data_index])
            data_index += 1
        if data_index < data_length:
            b = (b & ~1) | int(data[data_index])
            data_index += 1
        new_pixels.append((r, g, b))
        if data_index >= data_length:
            new_pixels.extend(pixels[len(new_pixels):])
            break

    watermarked_image = Image.new('RGB', image.size)
    watermarked_image.putdata(new_pixels)

    # Map JPG to JPEG for Pillow compatibility
    extension = output_image_path.split('.')[-1].lower()
    if extension == "jpg":
        extension = "jpeg"

    watermarked_image.save(output_image_path, format=extension.upper())


def extract_watermark(watermarked_image_path):
    image = Image.open(watermarked_image_path)

    # Convert to RGB regardless of format
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixels = list(image.getdata())
    binary_data = ''

    for pixel in pixels:
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)

    # Extract length of watermark (first 32 bits)
    watermark_length = int(binary_data[:32], 2)
    watermark_bits = binary_data[32:32 + watermark_length]
    watermark = binary_to_text(watermark_bits)
    return watermark
