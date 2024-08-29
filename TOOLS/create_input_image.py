from PIL import Image, ImageDraw

def create_input_image(image_path='input_image.jpg'):
    # Create a blank image with white background
    width, height = 400, 400
    image = Image.new('RGB', (width, height), color='white')
    
    # Draw some shapes or text on the image
    draw = ImageDraw.Draw(image)
    draw.rectangle([(50, 50), (350, 350)], outline="black", width=5)
    draw.text((150, 180), "Sample Image", fill="black")
    
    # Save the image
    image.save(image_path)
    print(f"Input image created and saved as {image_path}")

if __name__ == "__main__":
    create_input_image()
