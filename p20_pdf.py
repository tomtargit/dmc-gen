# pip install fpdf2

from fpdf import FPDF







def main():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(txt="hello world")
    pdf.output("hello_world.pdf")


if __name__ == '__main__':
    main()

