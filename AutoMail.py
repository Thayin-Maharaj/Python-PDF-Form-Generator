import os
from decouple import config
import smtplib
from email.message import EmailMessage
import numpy as np
import pandas
from datetime import datetime
from html_template import html_template

EMAIL_ADDRESS = config('EMAILADD')
EMAIL_PASSWORD = config('EMAILPASS')
MAIL_LIST = config('MAILLIST')
PDF_INV = config('PDFINV')
SERVER = config('SERVER')
PORT = config('PORT', cast=int)

class auto_Email:
    '''
        This class is adapted from a seperate auto emailer for fincon.
        The class requires only the WestulDatabaseOrd.csv and the pdf files generated
        from this .csv file then will send email out to the residents using their 
        corresponding emails.

    '''


    def __init__(self, email_add=EMAIL_ADDRESS, password=EMAIL_PASSWORD, mailing_list=MAIL_LIST, pdf_invoice=PDF_INV, server=SERVER, port=PORT):
        self.email_add = email_add
        self.password = password
        self.mailing_list = mailing_list
        self.pdf_invoice = pdf_invoice
        self.server = server
        self.port = port


    def login(self, msg):
        '''
            This function will login to the desired server and send any email that is 
            passed to it. Once complete it will return print message to indicate success.
        '''
        smtp = smtplib.SMTP(self.server, self.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(self.email_add, self.password)
        smtp.send_message(msg)

        return print('Mail has been sent!')



    def create_msg(self, receiver, path, pdfname, ContactName, MonthYear):
        '''
            This function will create the message and search for the 
            appropriate pdf to attach to the message using the path variable
            the path variable is obtained from the get_path function
        '''

        msg = EmailMessage()
        msg['Subject'] = "Westul Estate Resident Information"
        msg['From'] = self.email_add
        msg['To'] = receiver
        html_msg = html_template()
        msg.set_content(html_msg, subtype='html')
        
        with open(path, 'rb') as f:
            file_data = f.read()
            
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=pdfname)
        return msg


    def get_path(self):
        '''
            This function will retrieve the paths where the pdfs that need to be
            sent are kept as well as returns an array of the account numbers and their 
            corresponding invoice number for this mouth using the mailling list.
        '''
        folder = os.getcwd()
        folder = os.path.join(folder, self.pdf_invoice)

        mail_list = pandas.read_csv(self.mailing_list)
        return mail_list, folder


    def send_Email(self):
        '''
            Sends an email after scanning the directory where the pdf is
            located using the account numbers from both the invoice data 
            and mailing list to check who needs an invoice.

            This will send one email per account number so the receipiant will
            recieve multiple emails if they require multiple invoices
        '''
        mail_list, folder = self.get_path()
        MonthYear = datetime.now().strftime("%B %Y")
        for i in range(0, len(mail_list)):
            filename = mail_list['FileName'][i]
            ContactName1 = mail_list['OwnerName'][i]
            # ContactName2 = mail_list['SpouseName'][i]
            receiver1 = mail_list['OwnerEmail'][i]
            # receiver2 = mail_list['SpouseEmail'][i]
            for entry in os.scandir(folder):
                if filename in entry.name:
                    path = os.path.join(folder, entry.name)
                    pdfname = entry.name
            if receiver1:
                msg = self.create_msg(receiver1, path, pdfname, ContactName1, MonthYear=MonthYear)
                print('Sending message to {}'.format(receiver1))
                try:
                    self.login(msg)
                except:
                    print("Message could not be sent to {}".format(receiver1))

            # if receiver2:
            #     msg = self.create_msg(receiver2, path, pdfname, ContactName2, MonthYear=MonthYear)
            #     print('Sending message to {}'.format(receiver2))
            #     try:
            #         self.login(msg)
            #     except:
            #         print("Message could not be sent to {}".format(receiver2))
            

                