# подключаем библиотеку для работы с базой данных
import sqlite3

# создаём класс для работы с базой данных
class DataBase:
    # конструктор класса
    def __init__(self):
        # соединяемся с файлом базы данных
        self.con = sqlite3.connect("Data Timer.db")
        # создаём курсор для виртуального управления базой данных
        self.cur = self.con.cursor()
        # если нужной нам таблицы в базе нет — создаём её
        self.cur.execute("""CREATE TABLE IF NOT EXISTS data(
                         timer TEXT,
                         month TEXT,
                         year INTEGER
                         );
                        """)

        # сохраняем сделанные изменения в базе
        self.con.commit()
    
    # деструктор класса
    def __del__(self):
        # отключаемся от базы при завершении работы
        self.con.close()

    # добавляем новую запись
    def insert(self, timer, month, year):
        # формируем запрос с добавлением новой записи в БД
        self.cur.execute("INSERT INTO data VALUES (?,?,?);", (timer, month, year))
        # сохраняем изменения
        self.con.commit()

    # Просмотр общего времени без привязки к году или месяцу
    def views_total_time(self):
        self.cur.execute("""WITH temp_seconds_minutes_hours AS (
                         SELECT 
                            SUM(CAST(SUBSTR(timer, 1, 2) AS INTEGER)) AS total_hours, 
                            SUM(CAST(SUBSTR(timer, 4, 2) AS INTEGER)) AS total_minutes, 
                            SUM(CAST(SUBSTR(timer, 7, 2) AS INTEGER)) AS total_seconds
                         FROM data
                         )
                         
                         -- Вывoд результатa сложения времени
                         SELECT 
                            total_hours || ':' ||
                            CASE WHEN LENGTH(total_minutes) = 1 THEN '0' || total_minutes ELSE total_minutes END || ':' ||
                            CASE WHEN LENGTH(total_seconds) = 1 THEN '0' || total_seconds ELSE total_seconds END AS total_time
                        FROM temp_seconds_minutes_hours;
                        """)
        rows = self.cur.fetchone()
        return rows
    

operation = DataBase()