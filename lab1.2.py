import math
import os
import pandas as pd
import base64


fileNames = ['Constitution - Ukraine.txt', 'Interview - Zelensky.txt', 'Motrya - Lepky.txt']
Base64Chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def Base64Coding(fileName):
    if '.bz2' in fileName:
        with open(fileName, 'rb') as file:
            text = file.read()
            text_bytes = bytearray(text)
    else:
        with open(fileName, 'r', encoding="utf-8") as file:
            text = file.read()
            text_bytes = bytearray(text.encode('cp1251'))


    bytesStr = ''
    for byte in text_bytes:
        bytesStr = bytesStr + ('0' * (8 - len(format(int(byte), 'b')))) + format(int(byte), 'b')

    base64Str = ''
    i = 0
    while i < len(bytesStr):
        base64Str = base64Str + Base64Chars[int(bytesStr[i: i + 6], 2)]
        i = i + 6


    if '.bz2' in fileName:
        with open(fileName[:-4] + '_Base64' + fileName[-4:], 'wb') as file:
            file.write(str.encode(base64Str))
    else:
        with open(fileName[:-4] + '_Base64' + fileName[-4:], 'w', encoding="utf-8") as file:
            file.write(base64Str)


def Calculations(fileName):
    # Відкриваємо файл, дістаємо звідти весь текст
    if '.bz2' in fileName:
        with open(fileName, 'rb') as file:
            text = file.read().decode()
    else:
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
              'InformationAmount': int(entropy * len(text) / 8)}
    return result


def entropyCalc(percents):
    res = 0
    for num in percents:
        if num != 0:
            res = res - (num * math.log2(num))
    return res


def ReadyCoding(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        text = file.read()

    encoded_text = text.encode('cp1251')
    ready64Str = base64.b64encode(encoded_text)

    with open(filename[:-4] + '_Ready64.txt', 'w', encoding="utf-8") as file:
        file.write(ready64Str.decode("UTF-8"))


def fileComparison(fileName1, fileName2):
    with open(fileName1, 'r', encoding="utf-8") as f1:
        text1 = f1.read()
        with open(fileName2, 'r', encoding="utf-8") as f2:
            text2 = f2.read()
    if text1 == text2:
        print(fileName1 + ' is equal to ' + fileName2)
    else:
        print(fileName1 + ' is not equal to ' + fileName2)



def main():
    # ---------------------- 2.2

    print('We encode the test file with a self-developed function')
    Base64Coding('Test.txt')
    print('File Test_Base64.txt is ready!')

    print('We encode the test file using a ready-made library')
    ReadyCoding('Test.txt')
    print('File Test_Ready64.txt is ready!')

    # Перевіряємо чи однаковий вміст цих файлів
    fileComparison('Test_Base64.txt', 'Test_Ready64.txt')

    # ---------------------- 2.3

    Base64Coding(fileNames[0])
    print('File ' + fileNames[0][:-4] + '_Base64.txt' + ' is ready!')
    Base64Coding(fileNames[1])
    print('File ' + fileNames[1][:-4] + '_Base64.txt' + ' is ready!')
    Base64Coding(fileNames[2])
    print('File ' + fileNames[2][:-4] + '_Base64.txt' + ' is ready!')


    Text1 = Calculations(fileNames[0][:-4] + '_Base64.txt')
    Text2 = Calculations(fileNames[1][:-4] + '_Base64.txt')
    Text3 = Calculations(fileNames[2][:-4] + '_Base64.txt')

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

    pages_sheets = {'General': page1, 'Text1Percents': page2, 'Text2Percents': page3, 'Text3Percents': page4,
                    'Entropy': page5}
    writer = pd.ExcelWriter('./statistic2.xlsx', engine='xlsxwriter')
    for page_name in pages_sheets.keys():
        pages_sheets[page_name].to_excel(writer, sheet_name=page_name, index=False)
    writer.save()

    # ---------------------- 2.4

    Base64Coding(fileNames[0][:-4] + '_Base64.txt.bz2')
    print('File ' + fileNames[0][:-4] + '_Base64.txt_Base64.bz2' + ' is ready!')
    Base64Coding(fileNames[1][:-4] + '_Base64.txt.bz2')
    print('File ' + fileNames[1][:-4] + '_Base64.txt_Base64.bz2' + ' is ready!')
    Base64Coding(fileNames[2][:-4] + '_Base64.txt.bz2')
    print('File ' + fileNames[2][:-4] + '_Base64.txt_Base64.bz2' + ' is ready!')

    Text1 = Calculations(fileNames[0][:-4] + '_Base64.txt_Base64.bz2')
    Text2 = Calculations(fileNames[1][:-4] + '_Base64.txt_Base64.bz2')
    Text3 = Calculations(fileNames[2][:-4] + '_Base64.txt_Base64.bz2')

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

    pages_sheets = {'General': page1, 'Text1Percents': page2, 'Text2Percents': page3, 'Text3Percents': page4,
                    'Entropy': page5}
    writer = pd.ExcelWriter('./statistic3.xlsx', engine='xlsxwriter')
    for page_name in pages_sheets.keys():
        pages_sheets[page_name].to_excel(writer, sheet_name=page_name, index=False)
    writer.save()


if __name__ == "__main__":
	main()