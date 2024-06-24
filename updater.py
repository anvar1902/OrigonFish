from clint.textui import progress
import time
import requests
import os



def updater():
    print("Начата установка новой версии ожидайте...")
    try:
        with open("latest_ver.txt", 'r') as file:
            data = file.readlines()
        os.remove("latest_ver.txt")
        LATEST_VERSION = data[0].replace("\n", "")
        URL = data[1].replace("\n", "")
        PROGRAM_NAME = data[2].replace("\n", "")

        r = requests.get(URL + f"/releases/download/{LATEST_VERSION}/{PROGRAM_NAME}", stream=True)

        if r.status_code == 200:
            total_length = int(r.headers.get('content-length'))

            with open(PROGRAM_NAME, 'wb') as file:
                for chunk in progress.bar(r.iter_content(chunk_size=1024), empty_char="-", width=50, expected_size=(total_length / 1024) + 1):
                    if chunk:
                        file.write(chunk)
                        file.flush()

            print("Новая версия успешно установлена запуск приложения через 5 секунд...")

        else:
            print('Не удалось установить новую версию программы пожалуйста обратитесь к разработчику за помощью либо обновите програму сами')

    except Exception as Error:
        print("Ошибка установки новой версии: \n", Error)
        print("Обратитесь за помощью к разработчику")

    time.sleep(5)
    os.startfile(PROGRAM_NAME)
    os.close(1)

if __name__ == "__main__":
    updater()
