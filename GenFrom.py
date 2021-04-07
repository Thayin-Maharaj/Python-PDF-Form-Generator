from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from pprint import pprint
import pandas as pd
import numpy as np
import os


def get_form_fields(infile):
    infile = PdfFileReader(open(infile, 'rb'))
    fields = PdfFileReader.getFields(infile)
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())


def set_need_appearances_writer(writer: PdfFileWriter):
    # See 12.7.2 and 7.7.2 for more information: http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer


def update_form_values(infile, outfile, newvals=None):
    pdf = PdfFileReader(open(infile, 'rb'), strict=False)
    if "/AcroForm" in pdf.trailer["/Root"]:
        pdf.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})
    else:
        print("pdf.trailer[/Root] does not exist")

    writer = PdfFileWriter()
    writer.cloneReaderDocumentRoot(pdf)
    set_need_appearances_writer(writer)
    if "/AcroForm" in writer._root_object:
        writer._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})
    else:
        print("/Acroform not in _root_object")

    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        try:
            if newvals:
                writer.updatePageFormFieldValues(page, newvals)
            # writer.addPage(page)
        except Exception as e:
            print(repr(e))
            # writer.addPage(page)
    
    with open(outfile, 'wb') as out:
        writer.write(out)
        writer.write(out)




def generate():
    pdf_file_name = 'Form_Final.pdf'

    # pprint(get_form_fields(pdf_file_name))


    data = pd.read_csv('Database/Database.csv')
    fields = dict(get_form_fields(pdf_file_name))
    cwd = os.getcwd()
    pdfpath = os.path.join(cwd, 'GeneratedForms/')

    for file in os.listdir(pdfpath):
        curfile = os.path.join(pdfpath, file)
        os.remove(curfile)

    for j in range(len(data)):
        for i in fields:
            if pd.isnull(data[i][j]):
                fields[i] = ''
            else:
                fields[i] = data[i][j]
    
        pdf_new_name = str(data['StreetNumber'][j])+'_'+str(data['StreetName'][j])+'_'+str(data['FamilyName'][j])
        infile = pdfpath + pdf_new_name+'.pdf'
        update_form_values(pdf_file_name, infile, fields)  # update the form fields
        data['FileName'][j] = pdf_new_name+'.pdf'
    data.to_csv('Database/Database.csv', index=None)        
