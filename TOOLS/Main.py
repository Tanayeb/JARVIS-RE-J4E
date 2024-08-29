from pdf_generator import PDFGenerator

def main():
    pdf_gen = PDFGenerator('output.pdf')
    
    # Add processed image
    pdf_gen.add_image('input_image.jpg')
    
    # Add processed text
    sample_text = """
    this is a sample text. it will be processed by the brain module.
    here is another sentence to demonstrate the processing capabilities.
    """
    pdf_gen.add_text(sample_text)
    
    # Save the PDF
    pdf_gen.save_pdf()

if __name__ == "__main__":
    main()
