from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- 1. Имитация Базы Данных (Database Service) ---
# Храним настройки и текущие показания датчиков в оперативной памяти
system_settings = {
    "min_temp": 18.0,
    "max_temp": 24.0,
    "theme": "light"
}

# Список объектов ("умных" школ и садов)
sensors_db = [
    {"id": 1, "name": "Школа №35", "temp": 24.5, "address": "ул. Ленина, 10"},
    {"id": 2, "name": "Монтажный техникум", "temp": 22.1, "address": "ул. Мира, 5"},
    {"id": 3, "name": "ДК учащейся молодёжи", "temp": 6.7, "address": "ул. Свободы, 12"}, # Авария (холодно)
    {"id": 4, "name": "Кубаньэнерго", "temp": 23.0, "address": "ул. Ставропольская, 2"},
    {"id": 5, "name": "Академия Стандарт", "temp": 29.0, "address": "ул. Красная, 100"}, # Авария (жарко)
]

# --- 2. Модуль Обработки Данных (Data Processing Unit) ---
def get_status(temp):
    """Функция определяет статус на основе настроек"""
    if temp < system_settings["min_temp"]:
        return "Ниже нормы", "red"
    elif temp > system_settings["max_temp"]:
        return "Выше нормы", "red"
    else:
        return "Норма", "green"

# --- 3. API Gateway и Маршрутизация ---

@app.route('/')
def index():
    """Страница авторизации (Auth Service UI)"""
    return render_template('login.html')

@app.route('/map')
def map_page():
    """Главная страница с картой"""
    return render_template('map.html')

@app.route('/settings')
def settings_page():
    """Страница настроек"""
    return render_template('settings.html', settings=system_settings)

# --- API Эндпоинты (для взаимодействия с JS) ---

@app.route('/api/objects', methods=['GET'])
def api_get_objects():
    """Возвращает список объектов с рассчитанными статусами"""
    response_data = []
    for sensor in sensors_db:
        status_text, color = get_status(sensor["temp"])
        response_data.append({
            "id": sensor["id"],
            "name": sensor["name"],
            "temp": sensor["temp"],
            "status": status_text,
            "color": color
        })
    return jsonify(response_data)

@app.route('/api/update_settings', methods=['POST'])
def api_update_settings():
    """Обновление порогов температуры"""
    data = request.json
    system_settings["min_temp"] = float(data.get("min", 18))
    system_settings["max_temp"] = float(data.get("max", 24))
    return jsonify({"success": True, "new_settings": system_settings})

if __name__ == '__main__':
    app.run(debug=True)
