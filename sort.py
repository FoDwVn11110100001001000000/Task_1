import sys, os, shutil
from transliterate import translit

folders = {
    ('doc','docx','txt','pdf','xlsx','pptx'): 'Documents',
    ('png','jpg','jpeg','svg'): 'Images',
    ('mp3','wav','amr','ogg'): 'Music',
    ('mp4','avi','mov','mkv'): 'Videos',
    ('zip','gz','tar'): 'Archive'
}

directory = fr'C:/Users{sys.argv[1]}'

def all_dir(directory):
    #проходимось по папці "Мотлох" рекурсивною функцією
    for dir, folder, file in os.walk(directory, topdown=False):

        #цикл перемістить усі файли у кореневу папку "Мотлох" та транслітить з кирилиці у латиницю
        #не зміг зробити через метод normalize, томущо видавало помилку "AttributeError: 'str' object has no attribute 'normalize'"
        #версія Python 3.11.3
        for f in file:
            try:
                x = translit(f'{f}', reversed=True)
                os.rename(f'{dir}/{f}' ,f'{directory}/{x}')
            except:
                os.rename(f'{dir}/{f}' ,f'{directory}/{f}')
        
        #так як ми перекинули всі файли у корінь "Мотлох", то інші папки вже пусті, їх можна видилити
        for dirs in folder:
            os.rmdir(f'{directory}/{dirs}')
        
        #створюємо папки задіюючи імена із словнику 'folders'
        for value in folders.values():
            full_path = os.path.join(directory, value)
            os.mkdir(full_path)
        
        #додаємо файли у відповідні папки, файли розширення яких невідомі, залишаються без змін.
        #також додаємо перевірку на розширення архівів, якщо архів то він розпаковує в відповідну папку, так видаляє zip-закінчення, та сам файл.
        for i in file:
            for key, value in folders.items():
                if i.endswith(key):
                    if value == 'Archive':
                        shutil.unpack_archive(f'{directory}/{i}', f'{directory}/Archive/{i[:-4]}')
                        os.remove(f'{directory}/{i}')

                    else:
                        shutil.move(f'{directory}/{i}', f'{directory}/{value}/{i}')

        

all_dir(directory) # python sort.py /"""ім'я юзера"""/Desktop/Мотлох





