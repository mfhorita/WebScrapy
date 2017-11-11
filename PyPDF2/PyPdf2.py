from PyPDF2 import PdfFileReader

arq = open(r'C:\Users\mfhor\Google Drive\Python\PyPDF2\ArqAux.txt', 'r') #C://Users//mfhor//Google Drive//Python//PyPDF2//Bacen.pdf
for line in arq:
    ArqPDf = line[0:-1]

pdf_file = open(ArqPDf, 'rb')
read_pdf = PdfFileReader(stream=pdf_file, strict=False)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()

with open(ArqPDf[0:-4] + '.txt', 'w') as f:
    f.write(page_content.__str__())