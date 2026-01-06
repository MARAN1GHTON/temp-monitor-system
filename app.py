import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DATABASE = 'system.db'

# Функция подключения к БД
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Позволяет обращаться к полям по имени
    return conn

# Настройки (пока оставим в памяти для простоты, или можно тоже в БД)
system_settings = {
    "min_temp": 18.0,
    "max_temp": 24.0
}

def get_status(temp):
    if temp < system_settings["min_temp"]:
        return "Ниже нормы", "red"
    elif temp > system_settings["max_temp"]:
        return "Выше нормы", "red"
    else:
        return "Норма", "green"

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/settings')
def settings_page():
    return render_template('settings.html', settings=system_settings)

# --- API: Получение списка объектов из БД ---
@app.route('/api/objects', methods=['GET'])
def api_get_objects():
    conn = get_db_connection()
    
    # Сложный запрос: берем объекты и приклеиваем к ним ПОСЛЕДНЮЮ температуру
    query = """
        SELECT o.id, o.name, o.address, r.temperature 
        FROM objects o
        JOIN readings r ON o.id = r.object_id
        WHERE r.id = (
            SELECT MAX(id) FROM readings WHERE object_id = o.id
        )
    """
    rows = conn.execute(query).fetchall()
    conn.close()

    response_data = []
    for row in rows:
        temp = row['temperature']
        status_text, color = get_status(temp)
        response_data.append({
            "id": row['id'],
            "name": row['name'],
            "temp": temp,
            "status": status_text,
            "color": color
        })
    
    return jsonify(response_data)

@app.route('/api/update_settings', methods=['POST'])
def api_update_settings():
    data = request.json
    system_settings["min_temp"] = float(data.get("min", 18))
    system_settings["max_temp"] = float(data.get("max", 24))
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
