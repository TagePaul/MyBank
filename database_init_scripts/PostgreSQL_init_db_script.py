#!/usr/local/bin/python
import os

def main():
    print('### Добрый день! Этот скрипт служит для:\n' \
          '### 1) Инициализация первой базы данных,\n' \
          '### 2) Установка пароля для роли postgres \n' \
          '### 3) Создания новой пользовательской роли с ' \
            'назначением всех прав на новую базу данных\n')

    postgres_password = input('### Введите пароль для роли postgres =>  ')
    database_name = input('### Введите название новой базы данных =>   ')
    name_new_role = input('### Введите имя новой роли =>   ')
    password_new_role = input(f'### Введите пароль для роли {name_new_role} =>   ')

    command_list = [
        {'command': f"ALTER ROLE postgres PASSWORD '{postgres_password}'",
         'db': 'postgres'
         },
        {'command': f"CREATE DATABASE {database_name}",
         'db': 'postgres'
         },
        {'command': f"CREATE ROLE {name_new_role} WITH LOGIN PASSWORD '{password_new_role}'",
         'db': 'postgres'
         },
        {'command': f"ALTER DATABASE {database_name} OWNER TO {name_new_role}",
          'db': 'postgres'
        },
        {'command': f"ALTER SCHEMA public OWNER TO {name_new_role}",
         'db': database_name}
    ]

    os.system("sudo sed -i '1s/^/local all all trust\\n/' /etc/postgresql/13/main/pg_hba.conf")
    os.system('sudo pg_ctlcluster 13 main reload')
    for command in command_list:
        os.system(f'''psql -U postgres -d {command["db"]} -c "{command["command"]}"''')
    os.system('sudo sed -i "1d" /etc/postgresql/13/main/pg_hba.conf')
    os.system('sudo pg_ctlcluster 13 main reload')

    ##Настройка что-бы postgres был виден из докера
    os.system("""sudo sed -i '1s/^/listen_addresses = "*"\\n/' /etc/postgresql/13/main/postgresql.conf""")
    os.system(f"sudo sed -i '1s/^/host  {database_name}  {name_new_role} 172.17.0.0/16  trust\\n/' /etc/postgresql/13/main/pg_hba.conf")
    os.system(f"sudo sed -i '1s/^/host  {database_name}  {name_new_role} 172.18.0.2/16  trust\\n/' /etc/postgresql/13/main/pg_hba.conf")
    os.system('sudo pg_ctlcluster 13 main reload')
if __name__ == '__main__':
    main()