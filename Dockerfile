# Используем легкий Python
FROM python:3.9-slim

# Рабочая папка внутри контейнера
WORKDIR /app

# Копируем все файлы проекта внутрь
COPY . .

# Устанавливаем Flask
RUN pip install flask

# Открываем порт 5000
EXPOSE 5000

# Команда запуска
CMD ["python", "app.py"]
