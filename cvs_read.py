import csv


def read_csv(file_name: str):
    with open('posts.csv', newline='', encoding='utf-8') as File:
        return list(csv.reader(File))[1:]
