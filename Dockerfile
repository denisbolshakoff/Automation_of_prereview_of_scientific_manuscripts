# Базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем пакеты и устанавливаем необходимые инструменты
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Скачиваем NLTK-данные
RUN python -m nltk.downloader punkt stopwords

# Открываем порт
EXPOSE 80

# Запускаем приложение
CMD ["python", "python-py.py"]