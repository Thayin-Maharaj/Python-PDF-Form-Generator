from UpdateDB import update
from GenFrom import generate
from AutoMail import auto_Email
import os
import time
print(
    '''
     _       _            _         _     ___   ___                                              
    ( )  _  ( )          ( )_      (_ )  (  _ \(  _ \  / \_/ \                                   
    | | ( ) | |  __   ___|  _)_   _ | |  | | ) | (_) ) |     |  _ _  ___    _ _   __    __  _ __ 
    | | | | | |/ __ \  __) | ( ) ( )| |  | | | )  _ (  | (_) |/ _  )  _  \/ _  )/ _  \/ __ \  __)
    | (_/ \_) |  ___/__  \ |_| (_) || |  | |_) | (_) ) | | | | (_| | ( ) | (_| | (_) |  ___/ |   
    \__/\___/ \____)____/\__)\___/(___) (____/(____/  (_) (_)\__ _)_) (_)\__ _)\__  |\____)_)   
                                                                              ( )_) |                        
                                                                               \___/            
                                                                             
    v0.2

    This Program enables easy management of the database containing the particulars of the 
    residents of Westul Estate.
    '''
)

while True:
    Ans = input(
'''
Please select an action from the following:

        Update the database from PDF files (U)
        Generate PDF Files from the existing database (G)
        Send Emails out to the residents (E)
        Quit (Q)

'''
            )

    if Ans == 'U' or Ans == 'u':
        print('Preparing to update')
        A1 = input('Are you sure that all PDFs are located in the WestulForms directory? (y/n)')
        if A1 == 'y' or A1 == 'Y':
            cwd = os.getcwd()
            path = os.path.join(cwd, 'WestulForms-Updated')
            if not os.listdir(path):
                print('\n\n No files in directory to update \n\n')
                time.sleep(0.5)
                continue
            else:
                print(os.listdir(path))
                update()
                print('All entries have been updated!')
            time.sleep(1)
        elif A1 == 'n' or A1 == 'N':
            continue
        else:
            print('Invalid response')
            continue
    
    elif Ans == 'G' or Ans == 'g':
        print('Generating forms from WestulDatabseOrd ...')
        time.sleep(0.5)
        generate()
        print("\n\n Forms have been generated! \n\n")
        time.sleep(1)
    
    elif Ans == 'E' or Ans == 'e':
        print('Starting Email service')
        auto_Email().send_Email()
        continue

    elif Ans == 'Q' or Ans == 'q':
        print('Exiting program ...')
        time.sleep(1)
        break
    
    else:
        print('Invalid input please enter a valid character from the list')
        continue