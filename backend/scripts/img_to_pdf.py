from PIL import Image
import os

def create_pdf_from_image(image_path, pdf_path):
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(pdf_path, "PDF", resolution=100.0)
        print(f"Successfully created {pdf_path}")
    except Exception as e:
        print(f"Error creating PDF: {e}")

if __name__ == "__main__":
    # Use the absolute path to the generated image
    image_path = "C:/Users/luckp/.gemini/antigravity/brain/b469802f-9045-4b90-94d2-1184b4c59012/sample_resume_pdf_1768140877113.png"
    pdf_path = "C:/Users/luckp/.gemini/antigravity/brain/b469802f-9045-4b90-94d2-1184b4c59012/sample_resume.pdf"
    create_pdf_from_image(image_path, pdf_path)
