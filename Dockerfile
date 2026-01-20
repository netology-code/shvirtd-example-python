FROM python:3.12

WORKDIR /app

# 1. Сначала копируем файл с зависимостями
COPY requirements.txt .

# 2. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем остальной код приложения
COPY . .

# Команда запуска (пример, может отличаться у вас)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
