#### JOSHUA RAMOS' FREEWAY TERROR ########

import csv

ACCOUNT_FILE = 'accounts.csv' #defining file name 

accounts = []

#taken from https://realpython.com/python-csv/#what-is-a-csv-file

def initAccounts():
    with open(ACCOUNT_FILE) as csv_file: # open file
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            record = [row[0], row[1], int(row[2])] # appened fields as element ot list
            accounts.append(record) #append list to accounts

            
def saveAccount():
    with open(ACCOUNT_FILE, mode='w') as csv_file: #open file 
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
        for a in accounts:
            writer.writerow(a) #rewrite with new data

