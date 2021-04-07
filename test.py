from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from pprint import pprint
import pandas as pd
import numpy as np
import os

data = pd.read_csv('WestulDatabaseOrd.csv')
pdfpath = os.getcwd()
pdf_new_name = 'Form_Final.pdf'

pdfread = PdfFileReader(open(pdf_new_name, 'rb'))
page = pdfread.getFields()

fields = pdf.trailer