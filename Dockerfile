FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=root:root --chmod=755 requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=root:root --chmod=755 manage.py .


COPY --chown=root:root --chmod=755 todo_project/ todo_project/

COPY --chown=root:root --chmod=755 todos/ todos/

RUN useradd -m django-user


USER django-user

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=todo_project.settings

EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]