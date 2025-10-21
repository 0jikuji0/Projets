from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

pdf.image("image.jpg", x=10, y=10, w=100)

pdf.set_font("Arial", size=12)
pdf.ln(60)

pdf.output("output.pdf")


print("image_pdf.pdf created successfully.")


