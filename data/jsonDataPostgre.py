
# УКАЗЫВАЙТЕ КОРРЕКТНЫЕ ДАННЫЕ ОТ БАЗЫ ЕСЛИ ЧТО-ТО НЕ ПОЛУЧАЕТСЯ И ЕСТЬ ВОПРОСЫ ПИШИТЕ @ProgramsCreator \ 
# SPECIFY THE CORRECT DATA FROM THE DATABASE IF SOMETHING DOES NOT WORK AND THERE ARE QUESTIONS, WRITE

data_base = {
            "postgreSQL": {
                "user": "postgres",
                "password": "", # password your db postgres \ ВВЕДИТЕ ПАРОЛЬ ЕСЛИ ОН ЕСТЬ ОТ БАЗЫ
                "host": "localhost",
                "port": 5432,
                "database": "" # ENTER THE DATABASE NAME! AND CREATE, IF THE DATABASE DOES NOT EXIST AND DO NOT CREATE TABLES, THEY WILL BE CREATED AUTOMATICALLY IN THE CREATED DATABASE \ 
                                   # ВВЕДИТЕ ИМЯ БАЗЫ ДАННЫХ! И СОЗДАЙТЕ, ЕСЛИ БАЗА ДАННЫХ НЕ СУЩЕСТВУЕТ И НЕ СОЗДАВАЙТЕ ТАБЛИЦЫ, ОНИ БУДУТ СОЗДАНЫ АВТОМАТИЧЕСКИ В СОЗДАННОЙ БАЗЕ ДАННЫХ
            }
        }
