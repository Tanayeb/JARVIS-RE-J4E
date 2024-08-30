from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from Backend.Brain import Brain

class PDFGenerator:
    def __init__(self, output_path):
        self.output_path = output_path
        self.brain = Brain()
        self.canvas = canvas.Canvas(output_path, pagesize=A4)
        self.width, self.height = A4

    def add_image(self, image_path, x=1*inch, y=5*inch, width=4*inch, height=4*inch):
        processed_image = self.brain.process_image(image_path)
        if processed_image:
            processed_image_path = 'processed_image.jpg'
            processed_image.save(processed_image_path)
            self.canvas.drawImage(processed_image_path, x, y, width=width, height=height)
        else:
            print("Failed to add image to PDF.")

    def add_text(self, text, x=1*inch, y=4*inch):
        processed_text = self.brain.process_text(text)
        text_object = self.canvas.beginText()
        text_object.setTextOrigin(x, y)
        text_object.setFont("Helvetica", 12)
        for line in processed_text.split('\n'):
            text_object.textLine(line)
        self.canvas.drawText(text_object)

    def save_pdf(self):
        self.canvas.save()
        print(f"PDF successfully saved to {self.output_path}")
