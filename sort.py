import sys, os, shutil
from transliterate import translit

name_folders = {
    ('doc','docx','txt','pdf','xlsx','pptx'): 'Documents',
    ('png','JPG','jpeg','svg'): 'Images',
    ('mp3','wav','amr','ogg'): 'Music',
    ('mp4','avi','mov','mkv'): 'Videos',
    ('zip','gz','tar'): 'Archive'
}

directory = fr'C:/Users{sys.argv[1]}'

def all_dir(directory):
    folders = []
    files = []
    #проходимось по папці "Мотлох" рекурсивною функцією, та зберігаємо результати у відповідні змінні
    if os.path.exists(directory):
        for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
            for folder in dirnames:
                folders.append(os.path.join(dirpath, folder))
            for file in filenames:
                files.append(os.path.join(dirpath, file))

    # цикл перемістить усі файли у кореневу папку "Мотлох" та транслітить з кирилиці у латиницю
    # не зміг зробити через метод normalize, томущо видавало помилку "AttributeError: 'str' object has no attribute 'normalize'"
    # версія Python 3.11.3
    # використовуючи метод "translit" також додаю exception, бо він не може визначити мову таких файлів, як "IMG_E7144" та подібних
    for f in files:
        path_file = os.path.basename(f)
        try:
            x = translit(path_file, reversed=True)
            os.rename(f ,f'{directory}/{x}')
        except:
            os.rename(f , f'{directory}/{path_file}')
    
    # так як ми перекинули всі файли у корінь "Мотлох", то інші папки вже пусті, їх можна видилити
    for fol in folders:
        os.rmdir(fol)
    
    #створюємо папки задіюючи імена із словнику 'folders'
    for value in name_folders.values():
        full_path = os.path.join(directory, value)
        os.mkdir(full_path)
    
    # додаємо файли у відповідні папки, файли розширення яких невідомі, залишаються без змін.
    # також додаємо перевірку на розширення архівів, якщо архів то він розпаковує в відповідну папку, так видаляє zip-закінчення, та сам файл.
    # використовуючи метод "translit" також додаю exception, бо він не може визначити мову таких файлів, як "IMG_E7144" та подібних
    for i in files:
        for key, value in name_folders.items():
            if i.endswith(key):
                try:
                    file_path = os.path.basename(i)
                    if value == 'Archive':
                        shutil.unpack_archive(f'{directory}/{translit(file_path, reversed=True)}', f'{directory}/Archive/{translit(file_path, reversed=True)[:-4]}')
                        os.remove(f'{directory}/{translit(file_path, reversed=True)}')
                    else:
                        shutil.move(f'{directory}/{translit(file_path, reversed=True)}', f'{directory}/{value}/{translit(file_path, reversed=True)}')
                except:
                    shutil.move(f'{directory}/{file_path}', f'{directory}/{value}/{file_path}')





all_dir(directory) # python sort.py /Bianchi/Desktop/Мотлох