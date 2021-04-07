from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader
from pprint import pprint
import pandas as pd
import numpy as np
import os
from datetime import date
import time

data = pd.read_csv('Database/WestulDatabaseOrd.csv')
pdfpath = os.getcwd()
westulforms = os.path.join(pdfpath, 'WestulForms-Updated')
today = date.today()
curdate = today.strftime("%B_%d_%Y")


def get_form_fields(infile):
    infile = PdfFileReader(open(infile, 'rb'))
    fields = infile.getFields()
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())


def update():
    if os.path.isfile("Database/WestulDatabaseUpdated_{}.csv".format(curdate)):
        df = pd.read_csv("Database/WestulDatabaseUpdated_{}.csv".format(curdate))
    else:
        df = data.drop(range(len(data)))

    for file in os.listdir(westulforms):
        curfile = os.path.join(westulforms, file)
        if file.endswith(".pdf"):
            print('\n\n Reading from file: {} \n\n'.format(file))
            time.sleep(0.1)
            fields = get_form_fields(curfile)
            df = df.append(fields, ignore_index=True)
            # try:
            #     fields = get_form_fields(curfile)
            #     df = df.append(fields, ignore_index=True)
            #     os.remove(curfile)
            # except:
            #     print("\nWARNING: File could not be read into DB.\n")
            #     time.sleep(2)
        else:
            #os.remove(curfile)
            print("\nWARNING: File {} is not in PDF format\n".format(file))
            time.sleep(2)
            continue

    df.to_csv('Database/WestulDatabaseUpdated_{}.csv'.format(curdate), index=False)