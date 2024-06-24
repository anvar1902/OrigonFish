from clint.textui import progress
import requests
import os

class Updater:
    def __init__(self, CURRECT_VERSION_str : str, repository_url : str, program_name : str, updater_name : str):
        self.CURRECT_VERSION_str = CURRECT_VERSION_str
        self.CURRECT_VERSION = list(map(int, CURRECT_VERSION_str.split('.')))
        self.LATEST_VERSION_str = None
        self.LATEST_VERSION = None
        self.VERSION_LEN = 3
        self.URL = repository_url
        self.PROGRAM_NAME = program_name
        self.UPDATER_NAME = updater_name
        print(f"Текущая версия программы: {self.CURRECT_VERSION_str}")

    def check_new_version(self):
        print("Проверка на наличие новой версии ожидайте...")

        try:
            latest_respone_url = requests.get(self.URL + "/releases/latest").url
            self.LATEST_VERSION_str = latest_respone_url.replace(self.URL + "/releases/tag/", '')
            self.LATEST_VERSION = list(map(int, self.LATEST_VERSION_str.split('.')))
            yn = ""
            for i in range(self.VERSION_LEN):
                if self.CURRECT_VERSION[i] + 1 <= self.LATEST_VERSION[i]:
                    print(f"Найдена новая версия: {self.LATEST_VERSION_str}")
                    yn = input("Хотите установить (Y/N)?: ").upper()

                    while yn != "Y" and yn != "N":
                        yn = input("Хотите установить (Y/N)?: ").upper()

                    if yn == "Y":
                        self.update_program()
                    return
            if yn == "":
                print("Последняя версия уже установлена")
                os.system("clear")
                os.system("cls")

        except Exception as Error:
            print("Ошибка проверки: \n", Error)
            print("Обратитесь за помощью к разработчику")

    def update_program(self):
        os.system("cls")
        os.system("clear")
        print("Начата установка новой версии")
        try:
            print("Скачивание Апдейтера")
            r = requests.get(self.URL + f"download/updater/updater.exe", stream=True)

            if r.status_code == 200 or 1:
                total_length = int(r.headers.get('content-length'))
                with open(self.UPDATER_NAME, 'wb') as file:
                    for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                              label='Скачивание Апдейтера',
                                              width=50,
                                              expected_size=(total_length / 1024) + 1):
                        if chunk:
                            file.write(chunk)
                            file.flush()

                print('Апдейтер успешно скачан\nЗапускаю Апдейтер')
                with open("latest_ver.txt", 'w') as file:
                    lines = [self.LATEST_VERSION_str, self.URL, self.PROGRAM_NAME]
                    file.writelines("%s\n" % line for line in lines)
                os.startfile(self.UPDATER_NAME)
                os.close(1)
            else:
                print('Не удалось скачать Апдейтер\nОтменяю обновление программы пожалуйста обратитесь к разработчику за помощью либо обновите програму сами')
        except Exception as Error:
            print("Ошибка установки новой версии: \n", Error)
            print("Обратитесь за помощью к разработчику")