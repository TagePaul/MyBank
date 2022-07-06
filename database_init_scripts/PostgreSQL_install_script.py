#!/usr/local/bin/python
import subprocess
import os

def main():
    result = subprocess.run(["which" ,"psql"], capture_output=True, text=True)
    if not result.stdout: # Проверка, установлен ли PostgreSQL
        # Установка PostgreSQL
        if z := input('PostgreSQL не установлен, для установки введи "Y" \n =>') == 'Y':
            print('Начинается установка PostgreSQL 13')
            command = "sudo sh -c 'echo " + '"deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" ' + "> /etc/apt/sources.list.d/pgdg.list'"
            result = os.system(command)

            result = os.system('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')
            result = os.system('sudo apt-get update')
            result = os.system('sudo apt-get -y install postgresql-13')
            result = os.system('sudo pg_ctlcluster 13 main start')

            result = subprocess.run(['sudo', 'pg_ctlcluster', '13', 'main', 'status'], capture_output=True, text=True)
            if result.stdout.startswith('pg_ctl: server is running'):
                print('PostgreSQL 13 установлен и запущен')
                return
            print('PostgreSQL установлен, но его не удалось запустить')
            return
        print('Отмена установки')
        return
    print('PostgreSQL уже установлен')
if __name__ == '__main__':
    main()
    # pg_ctl: server is running