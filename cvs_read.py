import csv


with open('posts.csv', newline='', encoding='utf-8') as File:
    file = list(csv.reader(File))[1:]
print(file[3])