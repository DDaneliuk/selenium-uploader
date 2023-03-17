import csv
from tempfile import NamedTemporaryFile
import shutil

def scan_one():
    fileId = ''
    with open('nft-list.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row[1] == '' and row[2] == '':
                fileId = row[0] 
                break

    return fileId           

def scan_one_delete():
    fileId = ''

    with open('clone.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if len(row) == 0:
                continue
            else:
                fileId = row[0] 
                return fileId

def scan():
    unuploaded_array = []
    with open('nft-list.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row[1] == '' and row[2] == '':
                unuploaded_array.append(row[0])
    return unuploaded_array     

def updater(id, title, url):
    tempfile = NamedTemporaryFile(mode="w", delete=False)
    fields = ["ID", "Title", "Url"]
    with open('nft-list.csv', 'r') as csv_file, tempfile:
        reader = csv.DictReader(csv_file, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['ID'] == str(id):
               new_data = [id, title, url]
               row['ID'], row['Title'], row['Url'] = new_data
            row = {
                "ID": row["ID"],
                "Title": row["Title"],
                "Url": row["Url"],
            }   
            writer.writerow(row)

    shutil.move(tempfile.name, "nft-list.csv")        
