import os
from PyPDF2 import PdfFileReader


# Bacen.pdf
path = os.path.dirname(os.path.realpath(__file__))
arq_pdf = open(path + '\\ArqAux.txt', 'r').read()

pdf = open(arq_pdf, 'rb')
read_pdf = PdfFileReader(stream=pdf, strict=False)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()

with open(arq_pdf[0:-4] + '.txt', 'w') as f:
    f.write(page_content.__str__())
