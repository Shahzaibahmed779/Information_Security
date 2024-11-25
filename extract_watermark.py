from watermarker import extract_watermark

def main():
    watermarked_image = watermarked_image = r'C:\Users\Mahnoor\Downloads\watermarked_original_image (1).png'
    extracted_text = extract_watermark(watermarked_image)
    print(f"Extracted Watermark: {extracted_text}")

if __name__ == "__main__":
    main()
