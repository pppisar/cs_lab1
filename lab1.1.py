import pandas as pd
import math
import os

fileNames = ['Constitution - Ukraine.txt', 'Interview - Zelensky.txt', 'Motrya - Lepky.txt']
alphabet = ''

def Calculations(fileName):
    # Відкриваємо файл, дістаємо звідти весь текст
    with open(fileName, 'r', encoding="utf-8") as file:
        text = file.read()
    alphabet = ''.join(sorted(set(text)))
    # Створюємо словник з статистикою знаходження символів в файлі
    letters = dict.fromkeys(alphabet, 0)
    # Підраховуємо скілки разів кожен символ зустрічається у тексті, пілся чого рахуємо відсоток
    for l in letters.keys():
        letters[l] = text.count(l) / len(text)
    #Створюємо словник, який буде містити розрахунки
    entropy = entropyCalc(list(letters.values()))
    result = {'letters': list(letters),
              'FileName': fileName,
              'TotalCount': len(text),
              'FileSize': os.path.getsize(fileName),
              'Percents': list(letters.values()),
              'Entropy': entropy,
              'InformationAmount': int(entropy * len(text) / 8),
              'ArchivesSize': [os.path.getsize(fileName + '.7z'),
                               os.path.getsize(fileName + '.bz2'),
                               os.path.getsize(fileName + '.gz'),
                               os.path.getsize(fileName + '.xz'),
                               os.path.getsize(fileName + '.zip')]}
    return result


def entropyCalc(percents):
    res = 0
    for num in percents:
        if num != 0:
            res = res - (num * math.log2(num))
    return res


def main():
    Text1 = Calculations(fileNames[0])
    Text2 = Calculations(fileNames[1])
    Text3 = Calculations(fileNames[2])

    page1 = pd.DataFrame({'indexes': ['Text1', 'Text2', 'Text3'],
             'File name': [Text1['FileName'], Text2['FileName'], Text3['FileName']],
             'Total characters': [Text1['TotalCount'], Text2['TotalCount'], Text3['TotalCount']],
             'File Size(bytes)': [Text1['FileSize'], Text2['FileSize'], Text3['FileSize']]})
    page2 = pd.DataFrame({'Letters': Text1['letters'],
                          'Percents': Text1['Percents']})
    page3 = pd.DataFrame({'Letters': Text2['letters'],
                          'Percents': Text2['Percents']})
    page4 = pd.DataFrame({'Letters': Text3['letters'],
                          'Percents': Text3['Percents']})
    page5 = pd.DataFrame({'indexes': ['Text1', 'Text2', 'Text3'],
                          'Entropy': [Text1['Entropy'], Text2['Entropy'], Text3['Entropy']],
                          'Information amount(bytes)': [Text1['InformationAmount'],
                                                       Text2['InformationAmount'],
                                                        Text3['InformationAmount']]})
    page6 = pd.DataFrame({'indexes': ['Text1', 'Text2', 'Text3'],
                          '.7z(bytes)': [Text1['ArchivesSize'][0], Text2['ArchivesSize'][0], Text3['ArchivesSize'][0]],
                          '.bz2(bytes)': [Text1['ArchivesSize'][1], Text2['ArchivesSize'][1], Text3['ArchivesSize'][1]],
                          '.gz(bytes)': [Text1['ArchivesSize'][2], Text2['ArchivesSize'][2], Text3['ArchivesSize'][2]],
                          '.xz(bytes)': [Text1['ArchivesSize'][3], Text2['ArchivesSize'][3], Text3['ArchivesSize'][3]],
                          '.zip(bytes)': [Text1['ArchivesSize'][4], Text2['ArchivesSize'][4], Text3['ArchivesSize'][4]]})

    pages_sheets = {'General': page1, 'Text1Percents': page2, 'Text2Percents': page3, 'Text3Percents': page4, 'Entropy': page5, 'Archives': page6}
    writer = pd.ExcelWriter('./statistic.xlsx', engine='xlsxwriter')
    for page_name in pages_sheets.keys():
        pages_sheets[page_name].to_excel(writer, sheet_name=page_name, index=False)
    writer.save()


if __name__ == "__main__":
	main()

