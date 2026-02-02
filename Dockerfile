FROM python:3.13-slim
LABEL authors="santamorina"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=todo_project.settings
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
]