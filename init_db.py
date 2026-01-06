import sqlite3

# Создаем файл базы данных
connection = sqlite3.connect('system.db')
cursor = connection.cursor()

# --- Удаляем старые таблицы (если есть), чтобы пересоздать чисто ---
cursor.execute('DROP TABLE IF EXISTS readings')
cursor.execute('DROP TABLE IF EXISTS objects')
cursor.execute('DROP TABLE IF EXISTS users')

# --- Создаем таблицы ---
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    latitude REAL,
    longitude REAL
)
''')

cursor.execute('''
CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id INTEGER NOT NULL,
    temperature REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (object_id) REFERENCES objects (id)
)
''')

# --- Наполняем данными (Школы и их температуры) ---
# 1. Добавляем объекты
objects_data = [
    ('Школа №35', 'ул. Ленина, 10', 55.75, 37.61),
    ('Монтажный техникум', 'ул. Мира, 5', 55.76, 37.62),
    ('ДК учащейся молодёжи', 'ул. Свободы, 12', 55.74, 37.60),
    ('Кубаньэнерго', 'ул. Ставропольская, 2', 55.77, 37.59)
]
cursor.executemany('INSERT INTO objects (name, address, latitude, longitude) VALUES (?, ?, ?, ?)', objects_data)

# 2. Добавляем температуры (последнее значение - актуальное)
# Для Школы 35 (id=1) - Норма
cursor.execute("INSERT INTO readings (object_id, temperature) VALUES (1, 23.0)")
cursor.execute("INSERT INTO readings (object_id, temperature) VALUES (1, 24.5)")

# Для Техникума (id=2) - Норма
cursor.execute("INSERT INTO readings (object_id, temperature) VALUES (2, 22.1)")

# Для ДК (id=3) - АВАРИЯ (Холодно)
cursor.execute("INSERT INTO readings (object_id, temperature) VALUES (3, 8.0)")
cursor.execute("INSERT INTO readings (object_id, temperature) VALUES (3, 6.7)")

# Для Кубаньэнерго (id=4) - Норма
cursor.execute("INSERT INTO readings (object_id, temperature) VALUES (4, 23.0)")

connection.commit()
connection.close()
print("База данных system.db успешно создана и наполнена!")
