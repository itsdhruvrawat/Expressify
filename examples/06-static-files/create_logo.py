"""
Script to generate a simple logo image for the static files example
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create directory if it doesn't exist
    image_dir = os.path.join(os.path.dirname(__file__), 'public', 'images')
    os.makedirs(image_dir, exist_ok=True)
    
    # Define the output path
    out_path = os.path.join(image_dir, 'logo.png')
    
    # Check if file already exists
    if os.path.exists(out_path):
        print(f"Logo already exists at {out_path}")
        return
    
    # Create a new image with a white background
    width, height = 300, 150
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a blue rounded rectangle for the background
    draw.rectangle([(10, 10), (width-10, height-10)], fill='#0066cc', outline=None)
    
    # Add text
    try:
        # Try to use a font if available
        font = ImageFont.truetype("arial.ttf", 40)
        draw.text((width//2, height//2), "Expressify", fill="white", font=font, anchor="mm")
    except IOError:
        # Fall back to default font
        draw.text((width//2-60, height//2-20), "Expressify", fill="white")
    
    # Save the image
    img.save(out_path)
    print(f"Logo created at {out_path}")

if __name__ == "__main__":
    create_logo() 