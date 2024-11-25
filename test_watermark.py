from watermarker import embed_watermark, extract_watermark

def main():
    input_image = 'static/images/original_image.png'
    output_image = 'static/images/watermarked_test.png'
    watermark_text = 'test_user@example.com|1234567890'

    # Embed the watermark
    embed_watermark(input_image, output_image, watermark_text)
    print(f"Watermark embedded into {output_image}")

    # Extract the watermark
    extracted_text = extract_watermark(output_image)
    print(f"Extracted Watermark: {extracted_text}")

if __name__ == "__main__":
    main()
