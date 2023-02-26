import csv
from tempfile import NamedTemporaryFile
import shutil


def main():
    global filename, process_array

    filename = 'nft-list.csv'
    scan_start = 0
    scan_stop = 5000
    process_array=[]

    #scan(scan_start, scan_stop)
    #print(len(process_array))
    updater()


def scan(start, stop):
    unuploaded_array = []
    with open('nft-list.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count >= start:
                id = row[0]
                title = row[1]
                url = row[2]
                if title == '' and url == '':
                    unuploaded_array.append(id)
            line_count += 1
            if line_count == stop:
                break
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
