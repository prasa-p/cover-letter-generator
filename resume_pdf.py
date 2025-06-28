# importing required modules
import PyPDF2

def get_resume(resume):
    # creating a pdf file object
    pdfFileObj = open(resume, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)


    # creating a page object
    pageObj = pdfReader.pages[0]

    result = pageObj.extract_text()

    # closing the pdf file object
    pdfFileObj.close()

    return result
